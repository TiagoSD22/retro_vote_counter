# Vote Counter Application

A Python application that processes voting messages from text files and generates CSV reports with topics sorted by vote count.

## Features

- Parses text files containing voting messages
- Extracts topics and vote counts from messages
- Generates CSV output with voting results
- Sorts results by vote count (descending order)
- Provides summary statistics
- Includes error handling and logging

## Input Format

The application expects a text file with messages in the following format:

```
[Person Name]
[Timestamp]
[Topic Number]-[Topic Description]
[Topic Number]-[Topic Description]
...

:[Topic Number]:
[Vote Count]
:[Topic Number]:
[Vote Count]
...
```

### Example Input

```
Joao
2:45 PM
1-any text
2-any text
3-any text

:1:
5
:2:
12

Mike
2:46 PM
1-any text
2-any text

:2:
8
```

## Usage

### Basic Usage

```bash
python app.py --topics_file=topics.txt
```

### Advanced Usage

```bash
# Specify custom output file
python app.py --topics_file=topics.txt --output=results.csv

# Enable verbose logging
python app.py --topics_file=topics.txt --verbose
```

### Command Line Arguments

- `--topics_file` (required): Path to the input text file containing voting messages
- `--output` (optional): Output CSV file name (default: `voting_results.csv`)
- `--verbose` or `-v` (optional): Enable verbose logging

## Output Format

The application generates a CSV file with the following columns:

- `creator_name`: Name of the person who created the topic
- `topic_number`: Topic number within the message
- `votes`: Number of votes received
- `subject`: Topic description/subject

Results are sorted by vote count in descending order.

### Example Output

```csv
creator_name,topic_number,votes,subject
Sarah,3,23,Python Performance Optimization
Sarah,1,15,Machine Learning Applications
Joao,2,12,any text
David,2,11,Cloud Computing Solutions
Mike,2,8,any text
Sarah,2,7,Data Analysis Best Practices
Joao,1,5,any text
David,1,3,Web Development Trends
```

## Requirements

- Python 3.7 or higher
- No external dependencies (uses only standard library)

## Installation

1. Clone or download the project files
2. Ensure Python 3.7+ is installed
3. No additional packages need to be installed

## Testing

A sample input file (`sample_topics.txt`) is provided for testing:

```bash
python app.py --topics_file=sample_topics.txt
```

## Error Handling

The application includes comprehensive error handling for:

- File not found errors
- Invalid file formats
- Parsing errors
- CSV generation errors

## Logging

The application uses Python's logging module to provide:

- Info level logging by default
- Debug level logging with `--verbose` flag
- Timestamps and log levels in output
- Error tracking and reporting

## Project Structure

```
vote_counter/
├── app.py                    # Main application file
├── sample_topics.txt         # Sample input file for testing
├── requirements.txt          # Python dependencies (none required)
├── README.md                 # This file
└── .github/
    └── copilot-instructions.md  # Copilot customization instructions
```

## Code Style

The code follows PEP 8 conventions and includes:

- Type hints for better code clarity
- Dataclasses for structured data
- Comprehensive docstrings
- Clean, readable code structure
- Proper error handling
