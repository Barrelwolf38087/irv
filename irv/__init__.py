"""
A module to abstract the IRV (Instant-Runoff Voting) functionality from the bot logic.
It functions as a state machine to make the backend as flexible as possible.

  Creating a new poll:

  irv.Poll()
      .name("Poll Name") # Must be unique!\
      .description("Poll Description")\
      .option("Option 1")\
      .option("Option 2")\
      .option("Option 3")\
      .create()

  Adding votes (when a player executes the vote command):

  # The third parameter is a list of integers corresponding to the ballot options in the preferred order.
  # In this example, the user has voted for option 2 as their first choice and option 3 as their third choice.
  # Returns 0 on success
  # Returns -1 if the poll does not exist or has closed, -2 for an invalid user ID,
  # or -3 if the ballot was invalid (e.g. user listed a nonexistent option or duplicates)
  # TODO: Move documentation to function
  irv.vote("Poll Name", "User ID", [2, 1, 3])

  Delegating votes:

  # Transfers all "voting points" from Alice to Bob,
  # including any votes that were delegated to Alice by other users.
  # Returns -1 if the first user does not exist, -2 if the second one doesn't,
  # -3 if the delegation would cause a circular dependency, or 0 otherwise.
  irv.delegate("Alice", "Bob")

  # Revokes Alice's delegation, meaning that no one can vote on their behalf.
  irv.undelegate("Alice")

  Finalizing a poll:

  # Closes voting.
  # Returns the Poll object for easy chaining with Poll.results().
  irv.get_poll("Poll Name").finalize()

  Getting results:

  results = irv.get_poll("Poll Name").results()
"""

from irv.poll import *
from irv.db import get as get_poll
