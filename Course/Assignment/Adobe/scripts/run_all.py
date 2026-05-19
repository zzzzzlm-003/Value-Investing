"""
Run all Adobe Homework Q5-Q8 scripts.
Output: ADBE-Homework-Output.xlsx, images/
"""
import os
import subprocess

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = ["q5_asset_value", "q6_epv", "q7_growth"]


def main():
    print("=" * 60)
    print("Adobe Homework Q5-Q8 - Run All Scripts")
    print("=" * 60)
    for name in SCRIPTS:
        print(f"\n=== {name} ===")
        subprocess.run(
            ["python3", os.path.join(BASE, "scripts", f"{name}.py")],
            cwd=BASE,
            check=True,
        )
    print("\n" + "=" * 60)
    print("Done. Output: ADBE-Homework-Output.xlsx, images/")
    print("=" * 60)


if __name__ == "__main__":
    main()
