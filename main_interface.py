from podcast_download import run

query = str(input("Enter podcast name: "))
ep_no = int(input("Enter number of episodes to be downloaded: "))

run(query, ep_no)