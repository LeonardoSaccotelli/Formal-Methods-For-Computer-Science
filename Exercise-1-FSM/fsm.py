import json
import click


class FSM:
    def __init__(self, spec_file):
        # Load the FSM specification from the JSON file with exception handling
        try:
            with open(spec_file, 'r') as f:
                spec = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: The file '{spec_file}' was not found.")
        except json.JSONDecodeError:
            raise ValueError(f"Error: The file '{spec_file}' is not a valid JSON file or is malformed.")

        # Validate the required keys in the JSON
        required_keys = ["states", "alphabet", "transitions", "initialState", "acceptStates"]
        for key in required_keys:
            if key not in spec:
                raise ValueError(f"Error: Missing required key '{key}' in FSM specification.")

        self.states = spec["states"]
        self.alphabet = spec["alphabet"]
        self.transitions = spec["transitions"]
        self.initial_state = spec["initialState"]
        self.accept_states = set(spec["acceptStates"])
        self.current_state = self.initial_state

    def transition(self, input_symbol):
        """Perform a transition based on the input symbol."""
        for transition in self.transitions:
            if transition["from"] == self.current_state and transition["input"] == input_symbol:
                click.echo(f"Transitioning from {self.current_state} to {transition['to']} on input '{input_symbol}'")
                self.current_state = transition["to"]
                return
        click.echo(f"No valid transition from state '{self.current_state}' on input '{input_symbol}'")

    def run(self, inputs):
        """Process a sequence of inputs through the FSM."""
        click.echo(f"Initial state: {self.current_state}")
        for input_symbol in inputs:
            if input_symbol not in self.alphabet:
                click.echo(f"Invalid input '{input_symbol}' not in alphabet {self.alphabet}")
                return
            self.transition(input_symbol)

        click.echo(f"Final state: {self.current_state}")
        if self.current_state in self.accept_states:
            click.echo(f"The FSM has reached an accept state: {self.current_state}")
        else:
            click.echo(f"The FSM did not reach an accept state.")

    def print_model(self):
        """Print the FSM model details."""
        click.echo("FSM Model Loaded:")
        click.echo(f"  States: {self.states}")
        click.echo(f"  Alphabet: {self.alphabet}")
        click.echo(f"  Initial State: {self.initial_state}")
        click.echo(f"  Accept States: {self.accept_states}")
        click.echo("  Transitions:")
        for transition in self.transitions:
            click.echo(f"    {transition['from']} --{transition['input']}--> {transition['to']}")
