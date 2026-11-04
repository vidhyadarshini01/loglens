
import re
import csv
import json
import argparse


ERROR_PATTERNS = {
    "AUTH_001": {
        "pattern": r"authentication failed|invalid credentials",
        "cause": "Authentication or credential issue"
    },
    "NET_001": {
        "pattern": r"connection timed out|network timeout",
        "cause": "Network connectivity or timeout"
    },
    "PDF_001": {
        "pattern": r"pdf.*failed|failed.*pdf",
        "cause": "PDF processing issue"
    },
    "LIC_001": {
        "pattern": r"license.*expired|activation failed",
        "cause": "License or activation issue"
    },
    "GEN_001": {
        "pattern": r"\berror\b|\bexception\b",
        "cause": "General application error"
    }
}


def classify_log(line):
    for error_id, details in ERROR_PATTERNS.items():
        if re.search(details["pattern"], line, re.I):
            return error_id, details["cause"]

    return None, None


def analyze_logs(input_file):
    results = {}

    with open(input_file, encoding="utf-8",
              errors="replace") as file:
        for line in file:
            error_id, cause = classify_log(line)

            if error_id:
                if error_id not in results:
                    results[error_id] = {
                        "error_id": error_id,
                        "frequency": 0,
                        "likely_root_cause": cause,
                        "sample_message": line.strip()
                    }

                results[error_id]["frequency"] += 1

    return list(results.values())


def export_report(results, output_file):
    fields = [
        "error_id",
        "frequency",
        "likely_root_cause",
        "sample_message"
    ]

    if output_file.endswith(".json"):
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(results, file, indent=4)

    elif output_file.endswith(".csv"):
        with open(output_file, "w", newline="",
                  encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(results)

    else:
        raise ValueError("Use a .csv or .json output file")


def main():
    parser = argparse.ArgumentParser(
        description="LogLens - Support Log Analyzer"
    )

    parser.add_argument("input", help="Input log file")
    parser.add_argument(
        "-o", "--output",
        default="reports/report.csv",
        help="Output CSV or JSON report"
    )

    args = parser.parse_args()

    results = analyze_logs(args.input)
    export_report(results, args.output)

    print(f"Errors found: {len(results)}")
    print(f"Report saved to: {args.output}")


if __name__ == "__main__":
    main()
