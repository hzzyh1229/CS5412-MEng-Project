# CS5412-MEng-Project
_Cloud-based user interactive SDE Job Application Platform_


As an ant in a beehive, you have struck liquid gold. The deeper you delve, the more dense and succulent the honey is. Crawl and rock your way through sticky platforms and enemies towards the core of the hive to get a taste of the finest and most luscious honey the universe has to offer!

## Download:

-   Unavailable Yet :P

## Objective:

  Our project aims to build a Handshake-like software-engineer-oriented job board, where the users are able to view new job information more conveniently at one single place. What’s more, users can upload their own information such as their application status and timeline for each company. Users also have the choice to share their own information in exchange for the analyzed data from other users who are willing to share, such as the average time/percentage for getting/passing an OA/VO for a certain company.

## Application Details:

  Our project will mainly have three parts. \
    1. A real-time crawler (which we plan to use an existing service or a self-built tool using python libraries). \
    2. A website page that allows user interaction, which contains multiple functions and would be the main part of our project. \
    3. A database that serves as the storage tier and stores both the job and the user information.\
  The web crawler could be built using python libraries. We will search from popular job boards such as LinkedIn and Glassdoor, copying the title, description, link, etc. We plan to also use some techniques from data mining to determine whether the job supports sponsorship or not (which is an important factor for international students). The website mainly splits into several functions. First is the user login and profile page, which displays all the information users already entered. The user would be able to visualize their timeline for the job application via the user profile. Second is the information for all the companies including the posted date and detailed statistics. For the database, we plan to use a database like CosmosDB to implement, and we would also add multiple layers of cache before the final database for higher-performance retrieving.


## Team:

[Yihan Zhang](https://github.com/hzzyh1229) | Programmer \
[Shuyan Huang](https://github.com/JoyceHuangEC) | Programmer \
[Yuchen Qiu] | Programmer 
