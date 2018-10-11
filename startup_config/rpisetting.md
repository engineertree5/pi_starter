##RASPBERRY PI SETTINGS

# Change wireless mouse settings for Raspbian Version 9 (stretch)
If you are using a wireless mouse and are experiencing lag do the following
* open terminal
* modifiy the /boot/cmdline.txt as root
    * $ vi /boot/cmdline.txt
* go to the end of the line and add "usbhid.mousepoll=0" add a space after ...serial-consoles
* reboot the system
    * sudo reboot
* wireless mouse should be a bit more responseive. If still slow change the value from `0` to `1`
https://www.youtube.com/watch?v=NTylKIss2N4
