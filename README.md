# Doctor's Aid

Doctor's Aid is a small Python CLI project for managing a patient registry and generating diagnosis-related recommendations.

It lets you:

- record patients with diagnosis accuracy, disease incidence, and treatment risk
- remove patients from the registry
- calculate the probability of a disease for a patient
- generate a treatment recommendation based on the calculated probability
- print the current registry in a tabular view

## Requirements

- Python 3.10 or newer

## Run It

Interactive mode:

```bash
python doctors_aid.py
```

Process commands from a file:

```bash
python doctors_aid.py commands.txt
```

Pipe commands from standard input:

```bash
type commands.txt | python doctors_aid.py
```

## Commands

```text
create name, diagnosis_accuracy, disease_name, incidence, treatment_name, treatment_risk
remove name
probability name
recommendation name
list
help
exit
```

Example:

```text
create Hayriye, 0.999, Breast Cancer, 50/100000, Surgery, 0.40
probability Hayriye
recommendation Hayriye
list
```

## Notes

- Patient names are treated as unique identifiers.
- Probability and recommendation outputs follow the app's existing decision logic.