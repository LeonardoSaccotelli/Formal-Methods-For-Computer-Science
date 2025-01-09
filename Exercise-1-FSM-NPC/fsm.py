import json
import click
from graphviz import Digraph
import os


class FSM:
    def __init__(self, spec_file):
        try:
            with open(spec_file, 'r') as f:
                spec = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: The file '{spec_file}' was not found.")
        except json.JSONDecodeError:
            raise ValueError(f"Error: The file '{spec_file}' is not a valid JSON file or is malformed.")

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

    def get_valid_inputs(self):
        """Get all valid inputs for the current state."""
        valid_inputs = [t["input"] for t in self.transitions if t["from"] == self.current_state]
        return valid_inputs

    def transition(self, input_symbol):
        """Perform a transition based on the input symbol."""
        for transition in self.transitions:
            if transition["from"] == self.current_state and transition["input"] == input_symbol:
                click.secho(f"{self.current_state:>10} --{transition['input']}--> {transition['to']}", bold=True)
                self.current_state = transition["to"]
                return
        click.secho(f"No valid transition from state '{self.current_state}' on input '{input_symbol}'",
                    fg="red", bold=True)

    def run(self, inputs):
        """Process a sequence of inputs through the FSM."""
        click.secho(f"Initial state: {self.current_state}", bold=True)
        for input_symbol in inputs:
            if input_symbol not in self.alphabet:
                click.secho(f"Invalid input '{input_symbol}' not in alphabet {self.alphabet}",
                           fg="red", bold=True)
                return
            self.transition(input_symbol)

        self.print_acceptance()

    def print_acceptance(self):
        """Print whether the FSM ends in an accept state."""
        click.secho(f"Final state: {self.current_state}", bold=True)
        if bool(self.accept_states):
            if self.current_state in self.accept_states:
                click.secho(f"The FSM has reached an accept state: {self.accept_states}.", fg="green", bold=True)
            else:
                click.secho(f"The FSM did not reach an accept state: {self.accept_states}.", fg="red", bold=True)

    def print_model(self):
        """Print the FSM model details."""
        click.secho("FSM Model Loaded:", bold=True, fg="blue")
        click.secho(f"  States: {self.states}", bold=True)
        click.secho(f"  Alphabet: {self.alphabet}", bold=True)
        click.secho(f"  Initial State: {self.initial_state}", bold=True)
        click.secho(f"  Accept States: {self.accept_states}", bold=True)
        click.secho("  Transitions:", bold=True)
        for transition in self.transitions:
            click.secho(f"{transition['from']:>10} --{transition['input']}--> {transition['to']}", bold=True)

    def draw_model(self, output_file, size='15,15', dpi=300):
        """Draw the FSM with uniform node size and no text overlap."""

        # Create subfolder if it doesn't exist
        output_folder = 'fsm_output'
        os.makedirs(output_folder, exist_ok=True)

        # Set the full path for the output file, appending the subfolder
        output_path = os.path.join(output_folder, output_file)

        dot = Digraph(format='png')
        dot.attr(size=size, dpi=str(dpi), rankdir='LR')  # Set the size, DPI, and left-to-right layout
        dot.attr('graph', nodesep='1.5', ranksep='1.5')  # Increase spacing between nodes
        dot.attr('edge', fontsize='36', labelfontsize='36', labeldistance='10', penwidth='2')  # Reduce edge font size slightly

        dot.node('begin', '', shape='point')  # Invisible starting point
        dot.attr('node', fontsize='36', fixedsize='true',
                 width='2.5', height='2.5', margin='0.2', penwidth='2')  # Larger nodes and padding
        dot.edge('begin', self.initial_state, label='start')  # Arrow to initial state

        # Add states
        for state in self.states:
            shape = 'doublecircle' if state in self.accept_states else 'circle'
            dot.node(state, state, shape=shape)

        # Add transitions
        for transition in self.transitions:
            dot.edge(transition['from'], transition['to'], label=transition['input'])

        # Render the diagram
        dot.render(output_path, cleanup=True, view=True)
