"""
`tiktok_uploader` module for uploading videos to TikTok

Key Functions
-------------
upload_video : Uploads a single TikTok video
upload_videos : Uploads multiple TikTok videos
"""
from os.path import abspath, exists
from typing import List
import time

from selenium.common.exceptions import TimeoutException

from selenium import webdriver 
from selenium.webdriver.common.by import By

from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


from src.tiktok_uploader.browsers import get_browser
from src.tiktok_uploader.auth import AuthBackend
from src.tiktok_uploader import config, logger
from src.tiktok_uploader.utils import bold, green


def upload_video(filename=None, description='', username='',
                 password='', cookies='', sessionid=None, cookies_list=None, proxies_list=None, *args, **kwargs):
    """
    Uploads a single TikTok video.

    Conder using `upload_videos` if using multiple videos

    Parameters
    ----------
    filename : str
        The path to the video to upload
    description : str
        The description to set for the video
    cookies : str
        The cookies to use for uploading
    sessionid: str
        The `sessionid` is the only required cookie for uploading,
            but it is recommended to use all cookies to avoid detection
    """

    auth = AuthBackend(username=username, password=password, cookies=cookies,
                       cookies_list=cookies_list, sessionid=sessionid)

    # make a list of 5 of the same videos to upload
    videos = [ { 'path': filename, 'description': description } ]

    return upload_videos(
            videos=videos,
            auth=auth,
            *args, **kwargs
        )


def upload_videos(videos: list = None, auth: AuthBackend = None, browser='chrome',
                  browser_agent=None, on_complete=None, headless=False, num_retires : int = 1,proxies=None, *args, **kwargs):
    """
    Uploads multiple videos to TikTok

    Parameters
    ----------
    videos : list
        A list of dictionaries containing the video's ('path') and description ('description')
    browser : str
        The browser to use for uploading
    browser_agent : selenium.webdriver
        A selenium webdriver object to use for uploading
    on_complete : function
        A function to call when the upload is complete
    headless : bool
        Whether or not the browser should be run in headless mode
    num_retries : int
        The number of retries to attempt if the upload fails
    options : SeleniumOptions
        The options to pass into the browser -> custom privacy settings, etc.
    *args :
        Additional arguments to pass into the upload function
    **kwargs :
        Additional keyword arguments to pass into the upload function

    Returns
    -------
    failed : list
        A list of videos which failed to upload
    """
    videos = _convert_videos_dict(videos)

    if videos and len(videos) > 1:
        logger.debug("Uploading %d videos", len(videos))

    if not browser_agent: # user-specified browser agent
        logger.debug('Create a %s browser instance %s', browser,
                    'in headless mode' if headless else '')
        driver = test_user_agent()
        while driver is None:
            driver = test_user_agent()
    else:
        logger.debug('Using user-defined browser agent')
        driver = browser_agent

    # test
    # driver.get("https://whoer.net/")
    # time.sleep(20)
    # return 0

    driver = auth.authenticate_agent(driver)
    # options = webdriver.ChromeOptions()

    # if headless:
    #     options.add_argument('--headless')
    # if browser_agent:
    #     options.add_argument(f'user-agent={browser_agent}')
    failed = []
    # uploads each video
    for video in videos:
        try:
            path = abspath(video.get('path'))
            description = video.get('description', '')

            logger.debug('Posting %s%s', bold(video.get('path')),
            f'\n{" " * 15}with description: {bold(description)}' if description else '')

            # Video must be of supported type
            if not _check_valid_path(path):
                print(f'{path} is invalid, skipping')
                failed.append(video)
                continue

            complete_upload_form(driver, path, description,
                                 num_retires = num_retires, headless=headless, 
                                 *args, **kwargs)
            time.sleep(5) # add a 5 second sleep after each video upload
        except Exception as exception:
            logger.error('Failed to upload %s', path)
            logger.error(exception)
            failed.append(video)

        if on_complete is callable: # calls the user-specified on-complete function
            on_complete(video)

    if config['quit_on_end']:
        driver.quit()

    return failed

def test_user_agent():
    """
    Tests the user_agent function.
    """
    auth = AuthBackend(cookies='asset/cookies/ prize09pit.txt')

    driver = get_browser(name='chrome', headless=False)
    driver = auth.authenticate_agent(driver)
    driver.get(config['paths']['upload'])
    try:
        # if _ == 0:
        upload_box = WebDriverWait(driver, 70).until(
            EC.presence_of_element_located((By.XPATH, config['selectors']['upload']['upload_video']))
        )
        print("agent is good.")
        result = driver
    except TimeoutException:
        print("agent is not good.")
        result = None

    return result

def complete_upload_form(driver, path: str, description: str, headless=False, *args, **kwargs) -> None:
    """
    Actually uploades each video

    Parameters
    ----------
    driver : selenium.webdriver
        The selenium webdriver to use for uploading
    path : str
        The path to the video to upload
    """
    # _go_to_upload(driver)
    
    # _set_video(driver, path=path, description=description, *args, **kwargs)
    # _set_interactivity(driver, **kwargs)
    # _set_description(driver, description)
    # _post_video(driver)
    fcl(driver)

def is_divisible_by_3(n):
    # Convertir le nombre en chaîne de caractères
    s = str(n)

    # Calculer la somme des chiffres
    digit_sum = sum(int(d) for d in s)

    # Vérifier si la somme est divisible par 3
    return digit_sum % 3 == 0

def scroll_to_element(driver, element):
        """
    Scrolls the window to the specified element

    Parameters
    ----------
    driver : selenium.webdriver
        The selenium webdriver to use for scrolling
    element : selenium.webdriver.remote.webelement.WebElement
        The element to scroll to
    """
    

def fcl(driver):
    
    print (green("folow and like"))
    driver.get("https://www.tiktok.com/foryou?lang=en")
    wait = WebDriverWait(driver, 30)
    retry = 0
    # Wait for the main content div to appear
    # Wait for all the like buttons to appear
    glike = wait.until(EC.presence_of_all_elements_located((By.XPATH, config['selectors']['buttons']['like'])))

    print("glike:", glike)
    gf = wait.until(EC.presence_of_all_elements_located((By.XPATH, config['selectors']['buttons']['follow'])))
    # fixed_elements = driver.find_elements_by_css_selector('*[style*="position: absolute"]')
    # for element in fixed_elements:
    #     driver.execute_script("arguments[0].style.display = 'none';", element)
    interfering_element = driver.find_element(By.XPATH,"//div[contains(@class, 'DivBottomContainer')]")

    # Remove the interfering element from the DOM
    driver.execute_script("arguments[0].remove();", interfering_element)

    i = 0
    print("Number of elements in glike:", len(glike))
    for i in range(0, len(glike), 4):

        try:
            # Scroll to the button to make it visible
            actions = ActionChains(driver)
            print("Locating element")
            print(glike[i].get_attribute('textContent'))
            time.sleep(10)
            a = i//4
            gf[a].click()
            time.sleep(2)
            glike[i].click()
            time.sleep(10)
            
            driver.execute_script("arguments[0].scrollIntoView();", glike[i+1])
            # Click on the button
        except TimeoutException as e:
            print("Timed out waiting for elements to appear:", e)
        except Exception as e:
            print("An error occurred:", e)
    print("Follow and like done")
    time.sleep(2)
    fcl(driver)
    print("Zbiii")
    time.sleep(20)


def _go_to_upload(driver) -> None:
    """
    Navigates to the upload page, switches to the iframe and waits for it to load

    Parameters
    ----------
    driver : selenium.webdriver
    """
    logger.debug(green('Navigating to upload page'))

    driver.get(config['paths']['upload'])


def _set_description(driver, description: str) -> None:
    """
    Sets the description of the video

    Parameters
    ----------
    driver : selenium.webdriver
    description : str
        The description to set
    """
    if description is None:
        # if no description is provided, filename
        return

    logger.debug(green('Setting description'))

    saved_description = description # save the description in case it fails

    desc = driver.find_element(By.XPATH, config['selectors']['upload']['description'])

    # desc populates with filename before clearing
    WebDriverWait(driver, config['explicit_wait']).until(lambda driver: desc.text != '')

    _clear(desc)

    while description:
        try:
            nearest_mention = description.find('@')
            nearest_hash = description.find('#')

            if nearest_mention == 0 or nearest_hash == 0:
                desc.send_keys('@' if nearest_mention == 0 else '#')

                # wait for the frames to load
                time.sleep(config['implicit_wait'])

                name = description[1:].split()[0]
                if nearest_mention == 0: # @ case
                    mention_xpath = config['selectors']['upload']['mention_box']
                    condition = EC.presence_of_element_located((By.XPATH, mention_xpath))
                    mention_box = WebDriverWait(driver, config['explicit_wait']).until(condition)
                    mention_box.send_keys(name)
                else:
                    desc.send_keys(name)

                # time.sleep(config['implicit_wait'])

                if nearest_mention == 0: # @ case
                    mention_xpath = config['selectors']['upload']['mentions'].format('@' + name)
                    condition = EC.presence_of_element_located((By.XPATH, mention_xpath))
                else:
                    hashtag_xpath = config['selectors']['upload']['hashtags'].format(name)
                    condition = EC.presence_of_element_located((By.XPATH, hashtag_xpath))

                elem = WebDriverWait(driver, config['explicit_wait']).until(condition)

                # ActionChains(driver).move_to_element(elem).click(elem).perform()
                desc.send_keys(Keys.ENTER)

                description = description[len(name) + 2:]
            else:
                min_index = _get_splice_index(nearest_mention, nearest_hash, description)

                desc.send_keys(description[:min_index])
                description = description[min_index:]
        except Exception as exception:
            print('Failed to set ', name)
            description = description[len(name) + 1:]
            # _clear(desc)
            # desc.send_keys(description) # if fail, use saved description


def _clear(element) -> None:
    """
    Clears the text of the element (an issue with the TikTok website when automating)

    Parameters
    ----------
    element
        The text box to clear
    """
    element.send_keys(2 * len(element.text) * Keys.BACKSPACE)


def _set_video(driver, path: str = '', description: str = '', num_retries: int = 1, *args, **kwargs):
    """
    Sets the video to upload

    Parameters
    ----------
    driver : selenium.webdriver
    path : str
        The path to the video to upload
    num_retries : number of retries (can occassionally fail)
    """
    # uploades the element
    logger.debug(green('Uploading video file'))
    for _ in range(num_retries):
        try:
            # if _ == 0:
            upload_box = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, config['selectors']['upload']['upload_video']))
            )
            print (upload_box)
            upload_box.send_keys(path)
            # else:
            #     complete_upload_form(driver, path, description,
            #                      num_retries = num_retries, 
            #                      *args, **kwargs)
            
            # waits for the upload progress bar to disappear
            upload_progress = EC.presence_of_element_located(
                (By.XPATH, config['selectors']['upload']['upload_in_progress'])
                )
            # try:
            #     driver.find_element(
            #         By.XPATH, config['selectors']['upload']['process_confirmation']
            #     )
            #     print ("waaaa")
            #     return 1
            # except Exception as exception:
            #     print ("waaaa2")
            WebDriverWait(driver, config['explicit_wait']).until(upload_progress)
            WebDriverWait(driver, config['explicit_wait']).until_not(upload_progress)

            # waits for the video to upload
            

            # NOTE (IMPORTANT): implicit wait as video should already be uploaded if not failed
            # An exception throw here means the video failed to upload an a retry is needed

            upload_confirmation = WebDriverWait(driver, config['implicit_wait']).until(
                EC.presence_of_element_located(
                    (By.XPATH, config['selectors']['upload']['upload_confirmation'])
                )
            )
            # WebDriverWait(driver, config['explicit_wait']).until(upload_confirmation)

            # wait until a non-draggable image is found
            process_confirmation = EC.presence_of_element_located(
                (By.XPATH, config['selectors']['upload']['process_confirmation'])
                )
            WebDriverWait(driver, config['explicit_wait']).until(process_confirmation)
            return 0
        except TimeoutException:
            # If the element is not found within 5 seconds, this block will be executed
            print("Upload confirmation element not found within the specified time.")

        except NoSuchElementException as exception:
            print("zbiii")
        except Exception as exception:
            print(exception)

    raise FailedToUpload()


def _set_interactivity(driver, comment=True, stitch=True, duet=True, *args, **kwargs) -> None:
    """
    Sets the interactivity settings of the video

    Parameters
    ----------
    driver : selenium.webdriver
    comment : bool
        Whether or not to allow comments
    stitch : bool
        Whether or not to allow stitching
    duet : bool
        Whether or not to allow duets
    """
    try:
        logger.debug(green('Setting interactivity settings'))

        comment_box = driver.find_element(By.XPATH, config['selectors']['upload']['comment'])
        stitch_box = driver.find_element(By.XPATH, config['selectors']['upload']['stitch'])
        duet_box = driver.find_element(By.XPATH, config['selectors']['upload']['duet'])

        # xor the current state with the desired state
        if comment ^ comment_box.is_selected():
            comment_box.click()

        if stitch ^ stitch_box.is_selected():
            stitch_box.click()

        if duet ^ duet_box.is_selected():
            duet_box.click()

    except Exception as _:
        logger.error('Failed to set interactivity settings')


def _post_video(driver) -> None:
    """
    Posts the video by clicking the post button

    Parameters
    ----------
    driver : selenium.webdriver
    """
    logger.debug(green('Clicking the post button'))

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    wait = WebDriverWait(driver, 30)
    post = wait.until(EC.element_to_be_clickable((By.XPATH, config['selectors']['upload']['post'])))
    # Interact with the element
    post.click()

    # waits for the video to upload
    post_confirmation = EC.presence_of_element_located(
        (By.XPATH, config['selectors']['upload']['post_confirmation'])
    )

    try:
        WebDriverWait(driver, config['explicit_wait']).until(post_confirmation)
        logger.debug(green('Video posted successfully'))
    except TimeoutException:
        logger.error('TimeoutException: Video failed to post')


# HELPERS

def _check_valid_path(path: str) -> bool:
    """
    Returns whether or not the filetype is supported by TikTok
    """
    return exists(path) and path.split('.')[-1] in config['supported_file_types']


def _get_splice_index(nearest_mention: int, nearest_hashtag: int, description: str) -> int:
    """
    Returns the index to splice the description at

    Parameters
    ----------
    nearest_mention : int
        The index of the nearest mention
    nearest_hashtag : int
        The index of the nearest hashtag

    Returns
    -------
    int
        The index to splice the description at
    """
    if nearest_mention == -1 and nearest_hashtag == -1:
        return len(description)
    elif nearest_hashtag == -1:
        return nearest_mention
    elif nearest_mention == -1:
        return nearest_hashtag
    else:
        return min(nearest_mention, nearest_hashtag)

def _convert_videos_dict(videos_list_of_dictionaries) -> List:
    """
    Takes in a videos dictionary and converts it.

    This allows the user to use the wrong stuff and thing to just work
    """
    if not videos_list_of_dictionaries:
        raise RuntimeError("No videos to upload")

    valid_path = config['valid_path_names']
    valid_description = config['valid_descriptions']

    correct_path = valid_path[0]
    correct_description = valid_description[0]

    def intersection(lst1, lst2):
        """ return the intersection of two lists """
        return list(set(lst1) & set(lst2))

    return_list = []
    for elem in videos_list_of_dictionaries:
        # preprocesses the dictionary
        elem = {k.strip().lower(): v for k, v in elem.items()}

        keys = elem.keys()
        path_intersection = intersection(valid_path, keys)
        description_interesection = intersection(valid_description, keys)

        if path_intersection:
            # we have a path
            path = elem[path_intersection.pop()]

            if not _check_valid_path(path):
                raise RuntimeError("Invalid path: " + path)

            elem[correct_path] = path
        else:
            # iterates over the elem and find a key which is a path with a valid extension
            for _, value in elem.items():
                if _check_valid_path(value):
                    elem[correct_path] = value
                    break
            else:
                # no valid path found
                raise RuntimeError("Path not found in dictionary: " + str(elem))

        if description_interesection:
            # we have a description
            elem[correct_description] = elem[description_interesection.pop()]
        else:
            # iterates over the elem and finds a description which is not a valid path
            for _, value in elem.items():
                if not _check_valid_path(value):
                    elem[correct_description] = value
                    break
            else:
                elem[correct_description] = '' # null description is fine

        return_list.append(elem)

    return return_list

class DescriptionTooLong(Exception):
    """
    A video description longer than the maximum allowed by TikTok's website (not app) uploader
    """

    def __init__(self, message=None):
        super().__init__(message or self.__doc__)


class FailedToUpload(Exception):
    """
    A video failed to upload
    """

    def __init__(self, message=None):
        super().__init__(message or self.__doc__)
