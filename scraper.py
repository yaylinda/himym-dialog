import csv
import re
import requests


def write_csv(data):
  """ Writes a CSV file of the scripts data """

  with open('data.csv', 'w') as file:
    writer = csv.DictWriter(file, fieldnames=data[0].keys())
    writer.writeheader()
    for row in data:
      writer.writerow(row)


def get_html(url):
  """ Returns the HTML of the url page """

  r = requests.get(url, headers={
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
  })
  html = r.text

  return html


def parse_list_page_html(html):
  """ Parses a page for links to HIMYM episode dialogs """
  episode_list = []

  lines = html.split('\n')
  for line in lines:
    if 'class="topictitle"' in line and ' - ' in line and 'x' in line:
      datum = {}
      query = line.split('/viewtopic.php?f=177&amp;t=')[1].split('&amp;')[0]
      episode_season_str = line.split('class="topictitle">')[1].split(' - ')[0]
      season_str = episode_season_str.split('x')[0]
      episode_str = episode_season_str.split('x')[1]
      datum['query'] = query
      datum['season'] = int(season_str)
      datum['episode'] = int(episode_str)
      episode_list.append(datum)

  return episode_list


def parse_episode_page_html(season, episode, html):
  """ Parses a page for HIMYM episode speakers and dialogs """
  character_names = ["Ted", "Barney", "Robin", "Marshall", "Lily"]

  data = []

  lines = html.split('\n')

  start_parse_dialog = False

  for line in lines:

    if 'class="postbody"' in line:
      start_parse_dialog = True

    if start_parse_dialog and '<p>' in line and ':' in line:
      datum = {}
      datum['season'] = season
      datum['episode'] = episode

      dialog_str = line.split(':')[1].split('</p>')[0]
      dialog_str = re.sub(r'\([a-zA-Z ]*\)', '', dialog_str)
      dialog_str = dialog_str.strip()
      datum['dialog'] = dialog_str
      datum['num_words'] = len(dialog_str.split())

      speakers_str = line.split('<p>')[1].split(':')[0]
      if ',' in speakers_str:
        for speaker in speakers_str.split(','):
          speaker = speaker.strip()
          datum['speaker'] = speaker
      else:
        speaker = speakers_str.strip()
        datum['speaker'] = speaker

      data.append(datum)

  return data


def main():
  domain = "http://transcripts.foreverdreaming.org"
  base_list_path = "/viewforum.php?f=177&start="
  base_episode_path = "/viewtopic.php?f=177&t="
  num_pages = 9
  results_per_page = 25
  
  data = []
  for i in range(0, num_pages):
    offset = i * results_per_page
    list_page_url = domain + base_list_path + str(offset)
    list_page_html = get_html(list_page_url)
    print("\nParsing episode list results from: " + list_page_url)
    episode_page_info_list = parse_list_page_html(list_page_html)
    print("Got %d episode paths" % len(episode_page_info_list))

    for episode_page_info in episode_page_info_list:
      episode_page_url = domain + base_episode_path + episode_page_info['query']
      episode_page_html = get_html(episode_page_url)
      print("\tParsing episode dialog from: " + episode_page_url)
      episode_data = parse_episode_page_html(episode_page_info['season'], episode_page_info['episode'], episode_page_html)
      data.extend(episode_data)

  print('\nExporting data to CSV...')
  write_csv(data)

  print('\nDone!')


if __name__ == '__main__':
  main()