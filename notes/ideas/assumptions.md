
# Assumptions:
    # Regular case: Use the relevant article to draft a cited solution.
    # Conflicting articles: Show the article with more helpful votes first, but clearly flag the disagreement and show the other article too.
    # Tie or close vote counts: Show the more recently updated article first, while still flagging the disagreement.
    #
    # I assumed each article has a DATE, and a HELPFUL VOTE attribute. 
    # I also am assuming: If the counts are within 10% of the higher count, give the more recently updated article priority. So 20 versus 18 is exactly a 10% difference, and the newer article wins the ranking. If the gap is larger, the article with more helpful votes ranks first.
    # I assume that the copilot will compare only articles applicable to the same issue; when their helpful-vote counts differ by at most 10% of the higher count, rank the newer article first; always flag a contradiction for agent review. 
    # I know there's a limitation here, because older articles may tend to have more helpful scores simply because they've been around for longer, but I wanted to demonstrate that for an issue, if helpfulness is controlled for, recency should then take priority. 
    # I'm also assuming all the router models are the same, and the only variation is the Luzon Connect's understanding and advice of problems. 
    # I'm assuming these articles are meant to be read by workers at Luzon Connect, not directly by customers. 
    # I'm assuming each article has its own category. 
    # For the articles: Have a counter for each md file and everytime the file is deemed a soln, the counter goes up by 1.  This can mean users can select which is the most appropriate article themselves. 
    # Should use MM/DD/YYYY since thats the standard in the PH.

    # I'm assuming I can provide the local keys myself. 