#!/usr/bin/env python3
"""
Vote Counter Application

This application processes voting messages from a text file and generates a CSV report
with topics sorted by vote count.

Usage: python app.py --topics_file=topics.txt
"""

import argparse
import csv
import re
import sys
from dataclasses import dataclass
from typing import List, Dict, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class Topic:
    """Represents a topic with its metadata."""
    creator_name: str
    topic_number: int
    subject: str
    votes: int = 0


@dataclass
class Message:
    """Represents a message with its metadata."""
    author: str
    timestamp: str
    topics: Dict[int, str]  # topic_number -> subject
    votes: Dict[int, int]   # topic_number -> vote_count


class VoteCounter:
    """Main class for processing voting messages and generating reports."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.messages: List[Message] = []
        self.all_topics: List[Topic] = []
    
    def parse_file(self) -> None:
        """Parse the input file and extract messages."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Split content into message blocks
            message_blocks = self._split_into_message_blocks(content)
            
            for block in message_blocks:
                message = self._parse_message_block(block)
                if message:
                    self.messages.append(message)
                    
            logger.info(f"Parsed {len(self.messages)} messages from {self.file_path}")
            
        except FileNotFoundError:
            logger.error(f"File not found: {self.file_path}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Error reading file: {e}")
            sys.exit(1)
    
    def _split_into_message_blocks(self, content: str) -> List[str]:
        """Split content into individual message blocks."""
        # Remove empty lines and split by double newlines or name patterns
        lines = [line.strip() for line in content.split('\n')]
        
        blocks = []
        current_block = []
        
        for line in lines:
            if not line:  # Empty line
                continue
                
            # Check if this line looks like a name (not starting with digit or colon)
            # and we already have content in current_block
            if (current_block and 
                not re.match(r'^\d+[-:]', line) and  # Not a topic line
                not re.match(r'^:\d+:', line) and    # Not a vote line
                not re.match(r'^\d{1,2}:\d{2}\s*(AM|PM)', line)):  # Not a time line
                
                # This might be a new message, save current block
                blocks.append('\n'.join(current_block))
                current_block = [line]
            else:
                current_block.append(line)
        
        # Add the last block
        if current_block:
            blocks.append('\n'.join(current_block))
            
        return blocks
    
    def _parse_message_block(self, block: str) -> Optional[Message]:
        """Parse a single message block."""
        lines = [line.strip() for line in block.split('\n') if line.strip()]
        
        if len(lines) < 2:
            return None
            
        # First line should be the author name
        author = lines[0]
        
        # Second line should be the timestamp
        timestamp_match = re.match(r'(\d{1,2}:\d{2}\s*(AM|PM))', lines[1])
        if not timestamp_match:
            logger.warning(f"Could not parse timestamp from: {lines[1]}")
            return None
            
        timestamp = timestamp_match.group(1)
        
        # Parse topics and votes
        topics = {}
        votes = {}
        
        i = 2  # Start after name and timestamp
        while i < len(lines):
            line = lines[i]
            
            # Check for topic line (starts with number-)
            topic_match = re.match(r'^(\d+)-(.+)$', line)
            if topic_match:
                topic_num = int(topic_match.group(1))
                topic_subject = topic_match.group(2).strip()
                topics[topic_num] = topic_subject
            
            # Check for vote line (:number:)
            vote_match = re.match(r'^:(\d+):$', line)
            if vote_match:
                topic_num = int(vote_match.group(1))
                # Next line should be the vote count
                if i + 1 < len(lines):
                    try:
                        vote_count = int(lines[i + 1])
                        votes[topic_num] = vote_count
                        i += 1  # Skip the vote count line
                    except ValueError:
                        logger.warning(f"Could not parse vote count: {lines[i + 1]}")
            
            i += 1
        
        return Message(author=author, timestamp=timestamp, topics=topics, votes=votes)
    
    def process_messages(self) -> None:
        """Process all messages and create topic list."""
        for message in self.messages:
            for topic_num, subject in message.topics.items():
                votes = message.votes.get(topic_num, 0)
                
                topic = Topic(
                    creator_name=message.author,
                    topic_number=topic_num,
                    subject=subject,
                    votes=votes
                )
                self.all_topics.append(topic)
        
        # Sort topics by votes (descending) and then by creator name
        self.all_topics.sort(key=lambda x: (-x.votes, x.creator_name))
        
        logger.info(f"Processed {len(self.all_topics)} topics")
    
    def generate_csv(self, output_file: str = "voting_results.csv") -> None:
        """Generate CSV file with voting results."""
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header
                writer.writerow(['creator_name', 'topic_number', 'votes', 'subject'])
                
                # Write data
                for topic in self.all_topics:
                    writer.writerow([
                        topic.creator_name,
                        topic.topic_number,
                        topic.votes,
                        topic.subject
                    ])
            
            logger.info(f"CSV file generated: {output_file}")
            print(f"Results saved to {output_file}")
            
        except Exception as e:
            logger.error(f"Error generating CSV: {e}")
            sys.exit(1)
    
    def print_summary(self) -> None:
        """Print a summary of the results."""
        if not self.all_topics:
            print("No topics found.")
            return
            
        print(f"\nFound {len(self.all_topics)} topics from {len(self.messages)} messages:")
        print("-" * 80)
        print(f"{'Creator':<15} {'Topic#':<8} {'Votes':<8} {'Subject'}")
        print("-" * 80)
        
        for topic in self.all_topics[:10]:  # Show top 10
            subject = topic.subject[:40] + "..." if len(topic.subject) > 40 else topic.subject
            print(f"{topic.creator_name:<15} {topic.topic_number:<8} {topic.votes:<8} {subject}")
        
        if len(self.all_topics) > 10:
            print(f"... and {len(self.all_topics) - 10} more topics")


def main():
    """Main function to run the vote counter application."""
    parser = argparse.ArgumentParser(
        description="Process voting messages and generate CSV report"
    )
    parser.add_argument(
        '--topics_file',
        required=True,
        help='Path to the text file containing voting messages'
    )
    parser.add_argument(
        '--output',
        default='voting_results.csv',
        help='Output CSV file name (default: voting_results.csv)'
    )
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create and run vote counter
    counter = VoteCounter(args.topics_file)
    counter.parse_file()
    counter.process_messages()
    counter.print_summary()
    counter.generate_csv(args.output)


if __name__ == "__main__":
    main()
