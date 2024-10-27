
# Planning Creator

This project is a full-python application that creates a plan for a team of bartenders. It answers the school bar's need by automating the secretary's process of creating planning. 

This is a personal two-month project. 


## Demo

![](/Ressources/Readme_ressources/demo.gif)


## Rules Used in This Version of the App (V1.3):

- Someone cannot have two time slots on the same day.

- Someone cannot have a time slot when they are unavailable.

- There cannot be two cleaning tasks in a row.

- The person responsible for cleaning on Sundays is the one who has not performed this task for the longest time among the team members.

- Everyone has the same number of time slots and balanced coefficients. If someone has more time slots than others, it is because they had more slots a long time ago compared to the others. (last_Foyz_fucked)

- Specific to this version: The "mefos" cannot have a time slot on "mefo" day. However, the "mefos" are not considered time slots. Therefore, they will have the same number of slots as others PLUS their "mefo" evening. TODO: Ensure they have fewer slots (this will be addressed in the next version, but currently, there's a bug where the computer often adds people to S3 on "mefo" evenings even when it is unnecessary).


## New Features in Version 1.4

- The team is no longer limited to "Foy'z 25" but can be any team with members' names specified in the "Team-data.xlsx" Excel file.

- The "mefos" can be specified in the Excel file or the application. They will not be assigned a time slot on "mefo" day. TODO: Ensure they have fewer slots (See TODO.md).


## Format of Compatible Excel Files

#### Unavailability File (Fichier des indispos)

- First solution
  
![App Screenshot](/Ressources/Readme_ressources/indispo_screen.png)
####

- Second solution
  
![App Screenshot](/Ressources/Readme_ressources/indispo_screen2.png)
####

#### Historical Data File (Fichier des historiques)
![App Screenshot](/Ressources/Readme_ressources/historic_screen.png)

The file names and their paths can be chosen at your convenience.


## Installation

```ruby
pip install numpy
pip install pandas
pip install openpyxl
pip install xlwings
pip install xlsxwriter
pip install selenium
pip install pillow
```


## Versions Historic

- V1.0 : first functioning version
- V1.1 : Could choose the number of workers on each time slot
- V1.2 : Could send their plannings to the  workers via Messenger
- V1.3
- V1.4 : Could be any Foy'z team (the workers' names should be written in the "team_data" excel file) and can take "Mefos" into account (the solution is not perfect as the "mefos" have the same amount of time slots than the others even if they have a "Mefo" to organize)



## Clients

<table>
  <tr>
    <td><img src="/Ressources/foyz1.png" alt="Image 1" width="100"/></td>
    <td><img src="/Ressources/Foyz (1).ico" alt="Image 1" width="100"/></td>
  </tr>
  <tr>
    <td> BDE ENSTA Bretagne (Club Foy'z) </td>
    <td> Foy'z 25 team</td>
  </tr>
</table>


## Authors

- [@Clem-Pat](https://www.github.com/Clem-Pat)
