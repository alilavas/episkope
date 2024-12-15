activate application "Messages"
tell application "System Events" to tell process "Messages"
	key code 45 using command down
	keystroke "[YourPhoneNumber]"
	key code 76
	do shell script "sleep 1"
	key code 76
	do shell script "sleep 1"
	keystroke "permit is availabe!"
	key code 76
end tell

