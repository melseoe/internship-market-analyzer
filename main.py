from take_post_urls_step_1 import take_posts
from take_post_details_step_2 import take_post_details
from analyze_data_step_3 import analysis

list_of_posts = take_posts()
detailed_list_of_posts = take_post_details(list_of_posts)
analysis(detailed_list_of_posts)