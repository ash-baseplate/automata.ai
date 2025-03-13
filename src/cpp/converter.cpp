/**
 * @file converter.cpp
 * @brief Implementation of NFA to DFA conversion using subset construction algorithm
 * 
 * This file contains the implementation of the NFA class and functions to:
 * - Input an NFA from user
 * - Display the NFA
 * - Convert the NFA to a DFA using the subset construction algorithm
 * - Display and visualize the resulting DFA
 */

#include <iostream>
#include <set>
#include <string>
#include <fstream>
#include <queue>
#include <stack>
#include <map>

/**
 * @class NFA
 * @brief Represents a Non-deterministic Finite Automaton
 */
class NFA{
public:
    std::set<std::string> states;                                          ///< Set of all states in the NFA
    std::set<char> symbols;                                                ///< Set of input symbols
    std::string startState;                                                ///< Start state of the NFA
    std::map<std::string, std::map<char, std::set<std::string>>> transactionState; ///< Transition function
    std::set<std::string> acceptingStates;                                ///< Set of accepting states

    /**
     * @brief Adds a transition to the NFA
     * @param fromstate The source state
     * @param symbol The input symbol
     * @param tostate The destination state
     */
    void addTransition(const std::string &fromstate, char symbol, const std::string &tostate){
        transactionState[fromstate][symbol].insert(tostate);
    }

    /**
     * @brief Displays the NFA details
     */
    void displayNFA(){

        std::cout<<"********************************************"<<std::endl;
        std::cout << "States: ";
        for (const auto &states : states)std::cout << states << " ";
        std::cout << "\n";

        std::cout << "\nSymbols: ";
        for (const auto &symbol : symbols)std::cout << symbol << " ";
        std::cout << "\n";

        std::cout << "\nstart state: ";
        std::cout << startState << " ";
        std::cout << "\n";

        std::cout << "\nTransition:\n";
        for (const auto &state : transactionState){
            for (const auto &symbol : state.second){
                std::cout << "From state " << state.first << " -> " << symbol.first << " -> ";
                for (const auto &toState : symbol.second){
                    std::cout << toState << " ";
                }
                std::cout << "\n";
            }
        }
        std::cout << "\n";

        std::cout << "acceptance state: ";
        for (const auto &accstate : acceptingStates)std::cout << accstate << " ";
        std::cout << "\n";

        std::cout<<"********************************************"<<std::endl;
    }

    /**
     * @brief Computes the epsilon closure of a state
     * @param state The state to compute epsilon closure for
     * @return Set of states reachable from the given state via epsilon transitions
     */
    std::set<std::string> epsilonClosure(const std::string &state) {
            std::set<std::string> closure; // Resulting closure set
            std::stack<std::string> stack; // Stack for processing states

            closure.insert(state); // Add the initial state to the closure
            stack.push(state);     // Push the state to the stack

            while (!stack.empty()) {
                std::string currentState = stack.top();
                stack.pop();

                // Check for epsilon transitions from the current state
                if (transactionState[currentState].count('#')) {
                    for (const auto &nextState : transactionState[currentState]['#']) {
                        if (closure.insert(nextState).second) { // If the state is newly added
                            stack.push(nextState); // Push it to the stack for further exploration
                        }
                    }
                }
            }

            return closure;
        }

    /**
     * @brief Converts the NFA to a DFA using subset construction algorithm
     * @return A map representing the DFA transitions
     */
    std::map<std::set<std::string>, std::map<char, std::set<std::string>>> convertToDFA() {
        std::map<std::set<std::string>, std::map<char, std::set<std::string>>> dfa;
        std::map<std::set<std::string>, std::string> stateNames;
        std::queue<std::set<std::string>> unprocessedStates;

        // Initialize with the start state (no epsilon closure)
        std::set<std::string> startStateSet = {startState};
        unprocessedStates.push(startStateSet);
        stateNames[startStateSet] = "q0";  // Assigning an arbitrary name to the start state

        // Processing states in the unprocessed queue
        while (!unprocessedStates.empty()) {
            std::set<std::string> currentState = unprocessedStates.front();
            unprocessedStates.pop();

            for (const char &symbol : symbols) {
                std::set<std::string> nextStates;
                for (const std::string &state : currentState) {
                    if (transactionState[state].count(symbol)) {
                        for (const std::string &nextState : transactionState[state][symbol]) {
                            nextStates.insert(nextState);  // No epsilon closure needed
                        }
                    }
                }

                if (!nextStates.empty() && dfa[currentState].count(symbol) == 0) {
                    dfa[currentState][symbol] = nextStates;
                    if (stateNames.count(nextStates) == 0) {
                        std::string newState = "q" + std::to_string(stateNames.size());
                        stateNames[nextStates] = newState;
                        unprocessedStates.push(nextStates);
                    }
                }
            }
        }

        return dfa;
    }
 
};

/**
 * @brief Takes input from user to construct an NFA
 * @param nfa Reference to an NFA object to be populated
 */
void inputNFA(NFA &nfa) {
    int numStates, numSymbols, numTransitions;
    std::string state, startState, acceptingState;

    // Taking states input
    std::cout << "Enter number of states: ";
    std::cin >> numStates;
    std::cout << "Enter states: ";
    for (int i = 0; i < numStates; i++) {
        std::cin >> state;
        nfa.states.insert(state);
    }

    // Taking symbols input
    std::cout << "Enter number of symbols: ";
    std::cin >> numSymbols;
    char symbol;
    std::cout << "Enter symbols (separate by space): ";
    for (int i = 0; i < numSymbols; i++) {
        std::cin >> symbol;
        nfa.symbols.insert(symbol);
    }

    // Taking start state input
    std::cout << "Enter start state: ";
    std::cin >> startState;
    nfa.startState = startState;

    // Taking accepting states input
    std::cout << "Enter number of accepting states: ";
    int numAcceptingStates;
    std::cin >> numAcceptingStates;
    std::cout << "Enter accepting states: ";
    for (int i = 0; i < numAcceptingStates; i++) {
        std::cin >> acceptingState;
        nfa.acceptingStates.insert(acceptingState);
    }

    // Taking transitions input
    std::cout << "Enter number of transitions: ";
    std::cin >> numTransitions;
    std::string fromState, toState;
    char transitionSymbol;
    for (int i = 0; i < numTransitions; i++) {
        std::cout << "Enter transition (fromState symbol toState): ";
        std::cin >> fromState >> transitionSymbol >> toState;
        nfa.addTransition(fromState, transitionSymbol, toState);
    }
}

/**
 * @brief Displays the conversion result and generates a DOT file for visualization
 * @param nfa Reference to the NFA object
 */
void displayConversion(NFA &nfa) {
    std::map<std::set<std::string>, std::map<char, std::set<std::string>>> dfa = nfa.convertToDFA();
    std::cout << "\nConverted DFA:\n";
    
    // Output to a .dot file for visualization
    std::ofstream dotFile("dfa.dot");
    dotFile << "digraph DFA {\n";
    dotFile << "    rankdir=LR;\n";  // Left to right layout
    
    // Map from set of NFA states to a unique DFA state name
    std::map<std::set<std::string>, std::string> stateNames;
    int stateCounter = 0;

    // First pass: Assign names to all states
    for (const auto &state : dfa) {
        if (stateNames.find(state.first) == stateNames.end()) {
            stateNames[state.first] = "q" + std::to_string(stateCounter++);
        }
    }

    // Add nodes for each state
    for (const auto &state : dfa) {
        std::string stateName = stateNames[state.first];
        std::string label = "{";
        for (const auto &st : state.first) {
            label += st + " ";
        }
        label += "}";

        // Check if this state contains any accepting states from NFA
        bool isAccepting = false;
        for (const auto &st : state.first) {
            if (nfa.acceptingStates.find(st) != nfa.acceptingStates.end()) {
                isAccepting = true;
                break;
            }
        }

        // Define node attributes
        dotFile << "    " << stateName << " [label=\"" << label << "\"";
        if (isAccepting) {
            dotFile << ", shape=doublecircle";
        } else {
            dotFile << ", shape=circle";
        }
        dotFile << "];\n";
    }

    // Add start state
    dotFile << "    start [shape=point];\n";
    std::set<std::string> startStateSet = {nfa.startState};
    if (stateNames.find(startStateSet) != stateNames.end()) {
        dotFile << "    start -> " << stateNames[startStateSet] << ";\n";
    }

    // Add transitions (using a set to prevent duplicates)
    std::set<std::string> addedTransitions;
    for (const auto &state : dfa) {
        std::string fromState = stateNames[state.first];
        for (const auto &symbol : state.second) {
            for (const auto &toStateSet : {symbol.second}) {  // Use set to handle multiple transitions
                std::string toState = stateNames[toStateSet];
                // Create a unique transition identifier
                std::string transition = fromState + symbol.first + toState;
                if (addedTransitions.insert(transition).second) {
                    dotFile << "    " << fromState << " -> " << toState 
                           << " [label=\"" << symbol.first << "\"];\n";
                }
            }
        }
    }

    dotFile << "}\n";
    dotFile.close();

    // Display DFA in console
    for (const auto &state : dfa) {
        std::cout << "State " << stateNames[state.first] << " { ";
        for (const auto &st : state.first) std::cout << st << " ";
        std::cout << "}:\n";
        for (const auto &symbol : state.second) {
            std::cout << "    On symbol '" << symbol.first << "' -> { ";
            for (const auto &toState : symbol.second) std::cout << toState << " ";
            std::cout << "}\n";
        }
    }
}

/**
 * @brief Main function to run the NFA to DFA converter
 * @return Exit status
 */
int main(){
    NFA nfa;
    inputNFA(nfa);
    nfa.displayNFA();
    displayConversion(nfa);

    return 0;
}