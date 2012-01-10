import QuestionParser as qp

# The number of unassigned users that should be ready at any point.
standby_threshold = 100

parser = qp.QuestionParser()

# STAGE 1: Replenish new user supply.
# Query the database to determine how many unassigned users are avail.
#   if num < threshold, let's generate more.

# For each question template that exists, parse the template for the
# new user.
# JSON-ify the VARIABLES dictionary that we get back and store that
# with the question.


# STAGE 2: Check for new questions
# Build list of all tid's that exist.
# Check whether each user has a question definition for each ID.

# If not, parse one for them and insert it.
