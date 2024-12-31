import click
import click
from fsm import FSM

@click.command()
@click.option('--file', required=True, type=click.Path(exists=True), help="Path to the FSM specification JSON file.")
@click.option('--string', required=True, help="Input string to process through the FSM.")
def main(file, string):
    """Experiment to run an FSM with a given input string."""
    try:
        # Initialize FSM from the specification file
        fsm = FSM(file)

        # Print the loaded FSM model
        fsm.print_model()

        # Convert the input string into a list of characters (symbols)
        inputs = list(string)

        # Run the FSM with the input sequence
        click.echo(f"\nProcessing input string: {inputs}")
        fsm.run(inputs)

    except (FileNotFoundError, ValueError) as e:
        click.echo(click.style(e, fg="red", bold=True), err=True)

if __name__ == "__main__":
    main()
