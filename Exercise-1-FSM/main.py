import click
from fsm import FSM

@click.command()
@click.option('--file', required=True, type=click.Path(exists=True), help="Path to the FSM specification JSON file.")
@click.option('--inputs', required=False, help="Delimited string of input symbols for batch mode (e.g., 'a,b,a').")
@click.option('--delimiter', required=False, help="Delimiter for separating symbols in the input string (e.g., ',').")
@click.option('--interactive', is_flag=True, help="Run the FSM in interactive mode.")
def main(file, inputs, delimiter, interactive):
    """Run the FSM in batch mode or interactive mode."""
    try:
        # Check for mutually exclusive modes
        if inputs and interactive:
            click.secho("Error: You cannot use both --inputs and --interactive at the same time.", fg="red", bold=True)
            return

        # Initialize FSM from the specification file
        fsm = FSM(file)

        # Print the loaded FSM model
        fsm.print_model()

        if interactive:
            # Interactive mode
            click.secho("\nInteractive Mode: Enter input symbols one by one. "
                        "Type 'exit' to quit.", fg="blue", bold=True)
            while True:
                user_input = input(click.style("Enter input symbol: ", fg="yellow", bold=True))
                if user_input.lower() == "exit":
                    break
                elif user_input not in fsm.alphabet:
                    click.secho(f"Invalid input '{user_input}'. Please enter a valid symbol "
                                f"from the alphabet {fsm.alphabet}.", fg="red", bold=True)
                else:
                    fsm.transition(user_input)

            # Print whether the FSM ended in an accept state
            fsm.print_acceptance()
        elif inputs:
            # Batch mode
            if not delimiter:
                click.secho("Error: A delimiter is required for batch mode (--delimiter).",
                            fg="red", bold=True)
                return

            click.secho("\nProcessing input in batch mode:", fg="blue", bold=True)

            # Split the input string using the provided delimiter
            input_list = inputs.split(delimiter)

            click.secho(f"Input: {input_list}", bold=True)

            # Validate the inputs
            if not all(isinstance(symbol, str) for symbol in input_list):
                click.secho("Error: All input symbols must be strings.", fg="red", bold=True)
                return

            # Process the list of inputs
            fsm.run(input_list)
        else:
            click.secho("Error: You must provide --inputs for batch mode or "
                        "use --interactive for interactive mode.", fg="red", bold=True)

    except (FileNotFoundError, ValueError) as e:
        click.echo(e)

if __name__ == "__main__":
    main()
