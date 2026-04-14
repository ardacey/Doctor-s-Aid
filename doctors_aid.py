from __future__ import annotations

from dataclasses import dataclass
import argparse
import sys
from pathlib import Path


@dataclass
class PatientRecord:
    name: str
    diagnosis_accuracy: float
    disease_name: str
    incidence_numerator: int
    incidence_denominator: int
    treatment_name: str
    treatment_risk: float

    def incidence_text(self) -> str:
        return f"{self.incidence_numerator}/{self.incidence_denominator}"

    def probability(self) -> float:
        wrong_diagnosis = 1 - self.diagnosis_accuracy
        incidence_rate = self.incidence_numerator / self.incidence_denominator
        return incidence_rate / (wrong_diagnosis + incidence_rate)


class DoctorAidApp:
    def __init__(self) -> None:
        self.records: dict[str, PatientRecord] = {}

    def create(self, record: PatientRecord) -> str:
        if record.name in self.records:
            return f"Patient {record.name} cannot be recorded due to duplication."

        self.records[record.name] = record
        return f"Patient {record.name} is recorded."

    def remove(self, name: str) -> str:
        if name not in self.records:
            return f"Patient {name} cannot be removed due to absence."

        del self.records[name]
        return f"Patient {name} is removed."

    def probability(self, name: str) -> str:
        record = self.records.get(name)
        if record is None:
            return f"Probability for {name} cannot be calculated due to absence."

        probability = record.probability() * 100
        probability_text = f"{probability:.2f}".rstrip("0").rstrip(".")
        return (
            f"Patient {name} has a probability of {probability_text}% of having "
            f"{record.disease_name.lower()}."
        )

    def recommendation(self, name: str) -> str:
        record = self.records.get(name)
        if record is None:
            return f"Recommendation for {name} cannot be calculated due to absence."

        if record.probability() < record.treatment_risk:
            return f"System suggests {name} NOT to have the treatment."

        return f"System suggests {name} to have the treatment."

    def list_records(self) -> list[str]:
        lines = [
            "Patient Name    Diagnosis Accuracy  Disease Name        Disease Incidence  Treatment Name      Treatment Risk",
            "---------------  ------------------  ------------------  -----------------  ------------------  --------------",
        ]

        for record in self.records.values():
            lines.append(
                f"{record.name:<15}  "
                f"{record.diagnosis_accuracy * 100:>18.2f}%  "
                f"{record.disease_name:<18}  "
                f"{record.incidence_text():<17}  "
                f"{record.treatment_name:<18}  "
                f"{record.treatment_risk * 100:>12.0f}%"
            )

        return lines


def parse_create_arguments(argument_text: str) -> PatientRecord:
    parts = [part.strip() for part in argument_text.split(",")]
    if len(parts) != 6:
        raise ValueError(
            "create requires six comma-separated values: "
            "name, diagnosis accuracy, disease name, incidence, treatment name, treatment risk"
        )

    name = parts[0]
    diagnosis_accuracy = float(parts[1])
    disease_name = parts[2]
    incidence_parts = parts[3].split("/")
    if len(incidence_parts) != 2:
        raise ValueError("incidence must use the format numerator/denominator")

    treatment_name = parts[4]
    treatment_risk = float(parts[5])
    return PatientRecord(
        name=name,
        diagnosis_accuracy=diagnosis_accuracy,
        disease_name=disease_name,
        incidence_numerator=int(incidence_parts[0]),
        incidence_denominator=int(incidence_parts[1]),
        treatment_name=treatment_name,
        treatment_risk=treatment_risk,
    )


def process_command(app: DoctorAidApp, line: str) -> list[str]:
    stripped = line.strip()
    if not stripped:
        return []

    command, _, rest = stripped.partition(" ")
    command = command.lower()

    if command == "create":
        return [app.create(parse_create_arguments(rest))]
    if command == "remove":
        return [app.remove(rest.strip())]
    if command == "probability":
        return [app.probability(rest.strip())]
    if command == "recommendation":
        return [app.recommendation(rest.strip())]
    if command == "list":
        return app.list_records()
    if command in {"help", "?"}:
        return [
            "Commands:",
            "  create name, diagnosis_accuracy, disease_name, incidence, treatment_name, treatment_risk",
            "  remove name",
            "  probability name",
            "  recommendation name",
            "  list",
            "  exit",
        ]
    if command in {"exit", "quit"}:
        raise SystemExit

    return [f"Unknown command: {stripped}"]


def iter_input_lines(source: str | None) -> list[str]:
    if source is None:
        if sys.stdin.isatty():
            return []
        return sys.stdin.read().splitlines()

    return Path(source).read_text(encoding="utf-8").splitlines()


def run(app: DoctorAidApp, lines: list[str]) -> None:
    for line in lines:
        try:
            for output_line in process_command(app, line):
                print(output_line)
        except ValueError as error:
            print(error)


def interactive_shell(app: DoctorAidApp) -> None:
    print("Doctor's Aid ready. Type 'help' for commands, or 'exit' to quit.")
    while True:
        try:
            line = input("> ")
        except EOFError:
            print()
            break

        try:
            for output_line in process_command(app, line):
                print(output_line)
        except ValueError as error:
            print(error)
        except SystemExit:
            break


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Doctor's Aid is a small patient registry and treatment recommendation demo."
    )
    parser.add_argument(
        "input_file",
        nargs="?",
        help="Optional path to a command file. If omitted, the app reads from standard input or starts interactive mode.",
    )
    args = parser.parse_args()

    app = DoctorAidApp()
    lines = iter_input_lines(args.input_file)

    if lines:
        run(app, lines)
    else:
        interactive_shell(app)


if __name__ == "__main__":
    main()