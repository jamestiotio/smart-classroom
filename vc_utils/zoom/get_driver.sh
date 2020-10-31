#!/bin/bash

echo "Made by James Raphael Tiovalen - https://github.com/jamestiotio"
echo ""

if [ ! -f "/usr/local/bin/geckodriver" ] && [ ! -f "/usr/bin/geckodriver" ] && [ ! -f "/usr/local/bin/chromedriver" ] && [ ! -f "/usr/bin/chromedriver" ] && [ ! -f "/usr/lib/chromium-browser/chromedriver" ]; then

    curl --silent "https://api.github.com/repos/mozilla/geckodriver/releases/latest" |
        grep '"tag_name":' |
        sed -E 's/.*"([^"]+)".*/\1/' |
        xargs -I {} curl -sOL "https://github.com/mozilla/geckodriver/releases/download/"{}"/geckodriver-"{}"-linux64.tar.gz"

    tar -xzf geckodriver-*-linux64.tar.gz
    rm geckodriver-*-linux64.tar.gz
    chmod +x geckodriver
    sudo mv geckodriver /usr/local/bin/

    if ! grep -q 'export PATH=$PATH:/usr/local/bin/geckodriver' ~/.bashrc; then

        echo 'export PATH=$PATH:/usr/local/bin/geckodriver' >>~/.bashrc
        source ~/.bashrc

    fi

    echo 'GeckoDriver has been successfully installed!'

else

    echo -e 'Local installation of GeckoDriver or ChromeDriver detected!\n'
    echo 'Please remember to set the $PATH environment variable to include the selected webdriver accordingly. Quitting...'

fi
