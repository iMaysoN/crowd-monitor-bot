import json
import re

import requests

from Main import logger

__project_id_pattern = re.compile('/project/(\\d*?)/')
__crowd_api_pattern = re.compile('<textarea>(.*)</textarea>')
__headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
}
__blueprint_to_api_request_by_project_id = "https://crowdrepublic.ru/x/project/{}?mode=normal&scenario%5B%5D=finance&scenario%5B%5D=basic"

__project_id_to_link = dict()


def get_id_from_message_with_web_link(message):
    result = re.search(__project_id_pattern, message)
    project_id = result.group(1)
    api_link = str(__blueprint_to_api_request_by_project_id).format(project_id)
    __project_id_to_link[project_id] = api_link
    logger.warning('For projectId {0} stored {1}'.format(project_id, api_link))


def get_project_via_api_by_id(project_id):
    logger.warning('Try get request with projectId: {}'.format(project_id))
    api_link = __project_id_to_link.get(project_id)
    logger.warning('Link for it: {}'.format(api_link))
    r = requests.get(api_link, headers=__headers)
    result = re.match(__crowd_api_pattern, r.text)
    text = result.group(1)  # убираем левые xml-скобки
    json_resp = json.loads(text)
    return json_resp["Project"]
