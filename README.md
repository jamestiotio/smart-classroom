# Smart Classroom

SUTD UROP: Using Sensors to Enhance Learning/Invigilation in Classrooms

## Table of Contents

- [Usage](#usage)
  * [Video Conference/Call Utilities](#vc-utils)
    - [Zoom](#zoom)
  * [Face Processing](#face-processing)
  * [Dashboard](#dashboard)
- [Stakeholders](#stakeholders)
- [Additional Resources](#additional-resources)

## Usage <a name="usage"></a>

### Video Conference/Call Utilities (`vc_utils`) <a name="vc-utils"></a>

#### Zoom <a name="zoom"></a>

> NOTE: Look into the [`zoomus`](https://github.com/prschmid/zoomus) Python client library and consider using it once it provides support for live-streaming (check the status of [this PR](https://github.com/prschmid/zoomus/pull/72)).

For now, we will be using Zoom as our video conference platform. Before setup, ensure that we have at least a Zoom Pro Account and login [here](https://zoom.us/signin) using our account credentials.

##### Zoom App Setup

To create the Zoom App, go to the [Zoom Marketplace](https://marketplace.zoom.us/develop/create) and create an **account-level** `OAuth` app to access Zoom's live streaming API endpoints.

Zoom App Configuration:

- Specify the `Redirect URL for OAuth` to be: `https://zoom.us/oauth/authorize`
- App Name: `Smart Classroom`
- Short Description: `Using sensors to enhance learning/invigilation in classrooms`
- Long Description: `Zoom App used to stream video data to the Python script, which would be connected to the face processing code, which would in turn pass the output data to the dashboard.`
- Developer Name: `James Raphael Tiovalen`
- Developer Email Address: `james_raphael@mymail.sutd.edu.sg`
- Whitelist URL: `https://zoom.us/oauth/`
- Event Subscriptions:
  * Subscription Name: `Meeting Live Stream`
    - `All users in the account`
    - Specify the `Event notification endpoint URL`
    - Event types:
      * Start Meeting (`start_meeting`)
- Scopes:
  * `meeting:read:admin`: To get notification of a meeting being started.
  * `meeting:write:admin`: To get video data stream to be used by the Python app.

After which, since this is an OAuth app, we would need to install the app manually on our Zoom account for the very first time (due to security reasons) by logging in into our Zoom Marketplace account and then going to `https://marketplace.zoom.us/develop/apps/<app-id>/activation` to click the `Install` button. Click the `Authorize` button when prompted.

> If signing in using a Google account, ensure that less secure app access is allowed [here](https://myaccount.google.com/lesssecureapps). If access into the Google account is still not allowed, try opening up a new window and log into [this webpage](https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?response_type=code&redirect_uri=https%3A%2F%2Fdevelopers.google.com%2Foauthplayground&client_id=407408718192.apps.googleusercontent.com&scope=email) first before going back to the Zoom website to try logging in using the specified Google account again. The `client_id` specified in the URL is of Google's OAuth 2.0 Playground service.

##### Zoom Meeting Setup (Admin)

We will be using Zoom Meetings for classroom lessons (instead of Webinars).

Follow the instructions presented [here](https://support.zoom.us/hc/en-us/articles/115001777826-Live-Streaming-Meetings-or-Webinars-Using-a-Custom-Service) to enable and set up custom live-streaming service for the corresponding Zoom Meetings.

Go to `Account Management` > [`Account Settings`](https://zoom.us/account/setting) > `In Meeting (Advanced)` > `Allow live streaming the meetings`, enable the setting's toggle and enable the `Custom Live Streaming Service` checkbox.

##### Zoom Meeting Setup (Host)

As the host, start the meeting and ensure that the meeting is up before the PATCH requests are being sent to Zoom's server (as detailed in the next section's steps). If everything went well after the PATCH requests are sent, a `LIVE on Custom Live Streaming Service` (or `LIVE on inc`) indicator should be shown on the top-left section of our Zoom Meeting's window/screen (just beside the green shield with checkmark logo of Meeting Information).

##### Zoom Script

> We are using `Ubuntu 20.04.1` as our Operating System. We can use a private VPS set up on DigitalOcean (as a Droplet) as our server.

Before running anything, set up a server (we are using NGINX with the RTMP protocol) and install the dependencies:

```console
sudo apt update
sudo apt upgrade
sudo apt install -y nginx libnginx-mod-rtmp git build-essential ffmpeg libpcre3 libpcre3-dev libssl-dev zlib1g-dev
pip3 install -r requirements.txt
```

Remember to configure our `nginx.conf` NGINX configuration file:

```
sudo nano /etc/nginx/nginx.conf
```

Add these lines to the end of the `nginx.conf` file (with the appropriate `<stream-key>` value, which is `livestream` in our case):

```
rtmp {
        server {
                listen 1935;
                chunk_size 4096;
                notify_method get;

                application live {
                        live on;
                        record off;
                        push rtmp://127.0.0.1:1935/live/<stream-key>
                }
        }
}
```

And then, restart NGINX:

```
sudo systemctl restart nginx
```

We would need to periodically obtain the OAuth Access Token by using the provided Client ID and Client Secret to the Authorize URL and provide a valid Access Token URL. For OAuth, since we would need JavaScript to be enabled, we would need to use Selenium and acquire an accompanying webdriver (such as `geckodriver` or `chromedriver`). To do that, run:

```console
chmod +x get_driver.sh
./get_driver.sh
```

To run the ZOOM VC script to prepare the Zoom App and send the start signal to initiate a livestream:

```console
python3 zoom.py
```

Login to our Zoom account on the popped-up browser that appeared. Do take note that access tokens expire after 1 hour.

##### Zoom Live Stream Data

To start processing the video stream data:

```console
python3 process.py
```

### Face Processing <a name="face-processing"></a>

Process face data using machine learning (PyTorch) for emotion detection, gaze tracking, head pose estimation and attention analysis.

### Dashboard <a name="dashboard"></a>

Display analysis output data on an elegant and beautiful dashboard to provide real-time feedback to the instructors during class.

## Stakeholders <a name="stakeholders"></a>

- Team Members:
  - [James Raphael Tiovalen](https://github.com/jamestiotio)
  - [Velusamy Sathiakumar Ragul Balaji](https://github.com/ragulbalaji)
  - [Kenneth Chin Choon Hean](https://github.com/UrFriendKen)
- Supervisor: [Prof. Kenny Choo](https://github.com/Amorpheum)

## Additional Resources <a name="additional-resources"></a>

More content coming soon!
