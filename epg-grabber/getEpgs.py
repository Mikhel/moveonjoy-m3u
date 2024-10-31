import os
import gzip
import xml.etree.ElementTree as ET
import requests

tvg_ids_file = os.path.join(os.path.dirname(__file__), 'tvg-ids.txt')
output_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'epg.xml')

def fetch_and_extract_xml(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch {url}")
        return None

    if url.endswith('.gz'):
        try:
            decompressed_data = gzip.decompress(response.content)
            return ET.fromstring(decompressed_data)
        except Exception as e:
            print(f"Failed to decompress and parse XML from {url}: {e}")
            return None
    else:
        try:
            return ET.fromstring(response.content)
        except Exception as e:
            print(f"Failed to parse XML from {url}: {e}")
            return None

def filter_and_build_epg(urls):
    with open(tvg_ids_file, 'r') as file:
        valid_tvg_ids = set(line.strip() for line in file)

    root = ET.Element('tv')

    for url in urls:
        epg_data = fetch_and_extract_xml(url)
        if epg_data is None:
            continue

        for channel in epg_data.findall('channel'):
            tvg_id = channel.get('id')
            if tvg_id in valid_tvg_ids:
                root.append(channel)

        for programme in epg_data.findall('programme'):
            tvg_id = programme.get('channel')
            if tvg_id in valid_tvg_ids:
                root.append(programme)

    tree = ET.ElementTree(root)
    tree.write(output_file, encoding='utf-8', xml_declaration=True)

    print(f"New EPG saved to {output_file}")

urls = [
    'https://epgshare01.online/epgshare01/epg_ripper_US1.xml.gz',
    'https://epgshare01.online/epgshare01/epg_ripper_US_LOCALS2.xml.gz',
    'https://epgshare01.online/epgshare01/epg_ripper_MX1.xml.gz',
    'https://epgshare01.online/epgshare01/epg_ripper_DUMMY_CHANNELS.xml.gz',
    'http://m3u4u.com/epg/jq2zy98d6es52d1knxr5',
    'https://epgshare01.online/epgshare01/epg_ripper_CL1.xml.gz',
    'https://epgshare01.online/epgshare01/epg_ripper_CO1.xml.gz',
]

if __name__ == "__main__":
    filter_and_build_epg(urls)
