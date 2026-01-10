"""CLI entry point for Spec & Test Generator."""

import argparse
import json
import sys
from pathlib import Path

from . import SpecTestGenerator, __version__


def main() -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="spec-test-generator",
        description="Generate requirements and test artifacts from PRDs",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "prd",
        type=Path,
        help="Path to PRD markdown file",
    )
    parser.add_argument(
        "--policy",
        type=Path,
        help="Path to policy YAML file (default: pragmatic internal)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("spec"),
        help="Output directory for artifacts (default: spec/)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON instead of generating markdown artifacts",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Use strict regulated policy preset",
    )

    args = parser.parse_args()

    # Determine policy path
    policy_path = args.policy
    if args.strict and not args.policy:
        skill_dir = Path(__file__).parent.parent.parent
        policy_path = skill_dir / "skills" / "spec-test-generator" / "policy" / "preset.strict.yaml"

    try:
        generator = SpecTestGenerator(
            prd_path=args.prd,
            policy_path=policy_path,
            output_dir=args.output,
        )

        result = generator.generate()

        if args.json:
            # Convert to serializable format
            output = {
                "requirements": [r.to_dict() for r in result["requirements"]],
                "test_plan": {
                    "strategy": result["test_plan"].strategy,
                    "test_data": result["test_plan"].test_data,
                    "environments": result["test_plan"].environments,
                    "non_functional": result["test_plan"].non_functional,
                },
                "test_cases": [t.to_dict() for t in result["test_cases"]],
                "traceability": [
                    {
                        "req_id": e.req_id,
                        "test_id": e.test_id,
                        "type": e.test_type.value,
                        "priority": e.priority.value,
                    }
                    for e in result["traceability"]
                ],
                "open_questions": result.get("open_questions", []),
                "assumptions": result.get("assumptions", []),
            }
            print(json.dumps(output, indent=2))
        else:
            artifacts = generator.write_artifacts(result)

            print(f"\n{'=' * 60}")
            print("Spec & Test Generation Complete")
            print(f"{'=' * 60}")
            print(f"PRD: {args.prd}")
            print()

            print("Summary:")
            print(f"  Requirements: {len(result['requirements'])}")
            print(f"  Test Cases:   {len(result['test_cases'])}")
            print(f"  Traceability: {len(result['traceability'])} mappings")
            print()

            if result.get("open_questions"):
                print(f"Open Questions: {len(result['open_questions'])}")
                print()

            print("Generated Artifacts:")
            for name, path in artifacts.items():
                print(f"  {name}: {path}")
            print()

        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
