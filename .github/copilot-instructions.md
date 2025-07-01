# Copilot Instructions

<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

This is a Python application for processing voting messages from text files and generating CSV reports.

## Project Context
- The application reads messages from a text file where each message contains:
  - Person's name
  - Timestamp
  - Numbered topics with descriptions
  - Vote counts for topics (marked with :number: format)
- The output is a CSV file with columns: creator_name, topic_number, votes, subject
- Results are sorted by vote count in descending order

## Code Style
- Follow PEP 8 conventions
- Use argparse for command-line arguments
- Include proper error handling and logging
- Write clean, readable code with appropriate comments
