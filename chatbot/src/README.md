# File Structure
The files are split into different components and different files for better modularization of the code.
## CSS files for front end.
For the colors of the two different front ends, Canada games and Brock Chatbots, we have two files 
`brockcolor.css` and `canadacolor.css` which holds the color for the appropriate websites.

## Chatbox 
The directory Chat box contains different components that is contained with the chatbox area, which includes, a clipbutton, the feed, the thinking animation, the zoomin, and the zoomout buttons. These offer functionality for the user.

## Language
This directory is used to store static words which appear on the front end. This is done so that we can support multiple languages in the future for this software. The way this is organized is, there exist 3 files, which are BrockInfo.js, CanadaInfo.js and Lanprocess.js
### BrockInfo.js and CanadaInfo.js
Below is given how the file is structured, where the primarily key represents which language these are going to be in, i.e. `en` and then it contains a dictionary for words within the actually frontend.<br/> 
``` json
"en":{
    "name":"BrockChatBOT",
      "message":"Hello! Welcome to the Brock chat bot! What can I help you with today?",
      "inputmessage":"Type a query here...",
      "disclaimer":"All information taken from Brock University",
      "helptext":"You can ask questions on topics like course scheduling, course prerequisites, exam schedules, transit options and more. For example: \"What are the prerequisites for BTEC 4P06?\" or \"Who teaches COSC 4P02?\"\n\nTo increase the font size of the chatbot interface, press the magnifier with the plus button at the top right of the chatbox. To decrease font size, press the magnifier with the minus button.\n\nTo copy the full text of the chat to clipboard, press the copy button at the top right of the chatbox.\n\nTo switch to the Canada Games version of the chatbot, press the \"Switch\" button.",
      "disclaimermenu":"Disclaimer",
      "disclaimertext":"This is scraped from brock websites",
      "aboutusmenu":"About",
      "aboutustext":"We are a group of people",
      "helpmenu":"Help",
      "mainhelpmenu":"Help Menu",
      "switchbutton":"Switch"
  }
  ``` 
below are the given definition of the words<br>
| Word | Usage |
| ------ | ------|
| Name | This is the name that is used for the chat bot |
| Message | This is the introduction message that is displayed |
| Inputmessage | This is the placeholder message that is used for the input bar |
| Disclaimer | This is the disclaimer information that is read when we go to the disclaimer menu |
| Helptext | This is the help message available to the user when they push the help me button in the menu.|
| disclaimermenu | This is the word displayed for the disclaimer button. |
| aboutusmenu | This is the word displayed for the about us button in the menu. |
|aboutustext | This is the message that is displayed when the about us button is pressed. | 
| Helpmenu | This is the word that is used for the help me button. |
| mainhelpmenu | This is the title for the help me menu when that pops up. |
| switchbutton | This is the word for the button that is used to switch between Canadagames chatbot and Brock chatbot. | 

### Lanprocess.js
This script identifies which url we are in, and go grabs the appropriate key from the file that is requested.

## Navbar
This directory contains all the components for the Navigation bar for the software.<br>
The only two components for the navbar is the backarrow, which is used to go back to the splash page, and the burgeritems, which is for the burger menu on the navbar.<br>

In addition to that, all the necessary functions to be run for the appropriate buttons should also exist within the burger.js. 
```javascript
<div className= "dropdown">
            <DropdownItem act = {()=>HelpButton(props.state, props.func , props.setmessage)}>
        </div>
```
new buttons can be added by adding 
> `<DropdownItem act = {() => nameeoffunction(parameters)}>`  To the div tags.

The Navbar also uses the [Popup](../src/popup/popUp.js) to display different popup for information, such as the help me button, the disclaimer button, and the about us button.

## Popup
This directory contains the component for building a popup for the appropriate button that is being pushed, the parameters that this is expecting is the title, and the message to be displayed, both of which has to be in text format.
 