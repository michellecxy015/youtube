import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import WebDriverException, TimeoutException


def open_browser(headless=True):
    """
    Opens a new automated browser window with specified ChromeDriver path and stability configurations.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--window-size=1920,1080")
    if headless:
        options.add_argument("--headless")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # Specify ChromeDriver path
    service = Service('/Users/mac/Downloads/chromedriver-mac-arm64/chromedriver')  # Update the path if necessary
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def handle_privacy_popup(driver):
    """
    Handles privacy popups on YouTube.
    """
    try:
        reject_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(., 'Reject all') or contains(., 'I agree') or contains(., 'Accept all')]")
            )
        )
        reject_button.click()
        time.sleep(2)
    except TimeoutException:
        print("No privacy popup found.")


def search_youtube(driver, query):
    """
    Searches YouTube for a query and retrieves the first 5 video IDs.
    """
    search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    driver.get(search_url)
    time.sleep(3)

    # Handle privacy popup
    handle_privacy_popup(driver)

    # Extract the first 5 video IDs
    video_ids = []
    try:
        videos = driver.find_elements(By.ID, "video-title")[:5]  # Extract the top 5 videos
        for video in videos:
            video_url = video.get_attribute("href")
            if video_url:
                video_id = video_url.split("v=")[1].split("&")[0]
                video_ids.append(video_id)
    except Exception as e:
        print(f"Error retrieving video IDs: {e}")
    return video_ids


def scrape_video_details(driver, video_id):
    """
    Extracts video details including title, channel name, views, and publish time for a given video.
    """
    video_details = {}

    # Extract video title
    try:
        title_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//h1/yt-formatted-string[@class="style-scope ytd-watch-metadata"]'))
        )
        video_details["Title"] = title_element.text
    except Exception as e:
        print(f"Error extracting title for video {video_id}: {e}")
        video_details["Title"] = "Unknown Title"

    # Extract channel name
    try:
        channel_name_element = driver.find_element(By.CSS_SELECTOR, 'div#text-container yt-formatted-string#text')
        video_details["Channel Name"] = channel_name_element.text
    except Exception as e:
        print(f"Error extracting channel name: {e}")
        video_details["Channel Name"] = "Unknown Channel"

    # Extract number of views
    try:
        views_element = driver.find_element(By.CSS_SELECTOR, 'yt-formatted-string#info span')
        video_details["Views"] = views_element.text
    except Exception as e:
        print(f"Error extracting views: {e}")
        video_details["Views"] = "Unknown Views"

    # Extract publish time
    try:
        publish_time_element = driver.find_element(By.XPATH, '//yt-formatted-string[@id="info"]//span[contains(text(), "前") or contains(text(), "ago")]')
        video_details["Publish Time"] = publish_time_element.text
    except Exception as e:
        print(f"Error extracting publish time: {e}")
        video_details["Publish Time"] = "Unknown Publish Time"

    return video_details

def scrape_recommendations(driver, video_id, depth, max_depth=10):
    """
    Scrapes the top 10 recommended videos for a given video ID and follows the first recommended video for deeper depths.
    """
    if depth > max_depth:
        return []

    video_url = f"https://www.youtube.com/watch?v={video_id}"
    recommendations = []

    try:
        # Load the video page
        driver.get(video_url)
    

        # Wait for the page to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "video-title")))

        # Extract current video details
        current_video_details = scrape_video_details(driver, video_id)

        # Fetch recommended videos
        recommended_videos = driver.find_elements(By.CSS_SELECTOR, "ytd-compact-video-renderer")

        # Extract details for the top 10 recommended videos
        for idx, video in enumerate(recommended_videos[:10]):
            try:
                # Extract video link
                video_link = video.find_element(By.CSS_SELECTOR, "#thumbnail").get_attribute("href")
                rec_video_id = video_link.split("v=")[1].split("&")[0]

                # Extract video title
                rec_title = video.find_element(By.ID, "video-title").text

                # Extract channel name
                rec_channel_name = video.find_element(By.CSS_SELECTOR, "ytd-channel-name").text

                # Extract views
                try:
                    rec_views = video.find_element(By.CSS_SELECTOR, "span.ytd-video-meta-block").text
                except:
                    rec_views = "Unknown Views"

                # Extract publish time
                try:
                    rec_publish_time = video.find_element(By.CSS_SELECTOR, "span.ytd-video-meta-block + span").text
                except:
                    rec_publish_time = "Unknown Publish Time"

                # Append recommendation details
                recommendations.append({
                    "Source Video ID": video_id,
                    "Source Title": current_video_details.get("Title", "Unknown"),
                    "Source Channel Name": current_video_details.get("Channel Name", "Unknown"),
                    "Source Views": current_video_details.get("Views", "Unknown"),
                    "Source Publish Time": current_video_details.get("Publish Time", "Unknown"),
                    "Target Video ID": rec_video_id,
                    "Target Title": rec_title,
                    "Target Channel Name": rec_channel_name,
                    "Target Views": rec_views,
                    "Target Publish Time": rec_publish_time,
                    "Depth": depth
                })

            except Exception as e:
                print(f"Error processing video at index {idx}: {e}")
                continue

        # Check if there are recommendations to follow
        if recommended_videos:
            # Get the first recommended video's ID
            first_video_link = recommended_videos[0].find_element(By.CSS_SELECTOR, "#thumbnail").get_attribute("href")
            next_video_id = first_video_link.split("v=")[1].split("&")[0]

            # Recursively scrape the first recommended video for the next depth
            child_recommendations = scrape_recommendations(driver, next_video_id, depth + 1, max_depth)
            recommendations.extend(child_recommendations)

    except TimeoutException:
        print(f"Timeout while loading recommendations for video {video_id}")
    except Exception as e:
        print(f"An error occurred for video {video_id}: {e}")

    return recommendations

def scrape_recommendations_for_seeds(driver, seed_video_ids, max_depth=10):
    """
    Scrapes recommendations for multiple seed videos.
    """
    all_recommendations = []
    for video_id in seed_video_ids:
        print(f"Processing seed video: {video_id}")
        recommendations = scrape_recommendations(driver, video_id, depth=1, max_depth=max_depth)
        all_recommendations.extend(recommendations)
    return all_recommendations


def save_to_csv(data, output_path):
    """
    Saves extracted data to a CSV file.
    """
    if not data:
        print("No recommendations found. Exiting.")
        return

    keys = data[0].keys()
    with open(output_path, 'w', newline='', encoding='utf-8') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    print(f"Data successfully saved to {output_path}")


def main():
    driver = open_browser(headless=False)
    try:
        query = "Travel in Paris"
        output_path = "/Users/mac/Downloads/youtube_recommendation_network_1.csv"
        max_depth = 10

        print(f"Processing query: {query}")
        seed_video_ids = search_youtube(driver, query)
        if not seed_video_ids:
            print("No seed videos found. Exiting.")
            return

        print(f"Seed video IDs: {seed_video_ids}")

        # Scrape recommendation network for all seed videos
        all_recommendations = scrape_recommendations_for_seeds(driver, seed_video_ids, max_depth=max_depth)

        # Save to CSV
        save_to_csv(all_recommendations, output_path)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()