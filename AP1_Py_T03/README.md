# Project 03 — Python_Bootcamp

**Summary:**  
In this project, you will learn how to create a web application in Python using Flask.

💡 [Click here](https://new.oprosso.net/p/4cb31ec3f47a4596bc758ea1861fb624) to share your feedback on this project. It’s anonymous and helps our team improve the learning experience. We recommend completing the survey right after finishing the project.

## Contents

  - [Chapter I](#chapter-i)
  - [Chapter II](#chapter-ii)
    - [General Information](#general-information)
    - [Topics to Study](#topics-to-study)
  - [Chapter III](#chapter-iii)
    - [Task 0. Project Setup](#task-0-project-setup)
    - [Task 1. Creating the Project Structure](#task-1-creating-the-project-structure)
    - [Task 2. Implementing the Domain Layer](#task-2-implementing-the-domain-layer)
    - [Task 3. Implementing the Datasource Layer](#task-3-implementing-the-datasource-layer)
    - [Task 4. Implementing the Web Layer](#task-4-implementing-the-web-layer)
    - [Task 5. Implementing the DI Layer](#task-5-implementing-the-di-layer)


## Chapter I

**Instructions**

1. Throughout the course, you will often feel uncertain and have limited information, but that's all part of the experience. Remember, the repository and Google are always there for you. So are your peers and Rocket.Chat. Talk. Search. Use your common sense. Don't be afraid to make mistakes.
2. Be mindful of your sources. Cross-check. Think critically. Analyze. Compare.
3. Read the tasks carefully, and then read them again.
4. Pay close attention to the examples, too. They may include information that is not explicitly stated in the task itself.
5. You may encounter inconsistencies when something in the task or example contradicts what you thought you knew. Try to figure them out. If you can't, write it down as an open question and resolve it as you go. Don't leave questions unresolved.
6. If a task seems unclear or impossible, it probably just feels that way. Break it down into parts. Most of them will make sense on their own.
7. You’ll encounter all kinds of tasks. The bonus ones are for those who are curious and detail-oriented. They’re optional and more challenging, but completing them gives you extra experience and insight.
8. Don't try to cheat the system or your peers. Ultimately, you'll only be cheating yourself.
9. Got a question? Ask the peer to your right. If that doesn't help, ask the peer to your left.
10. When asking for help, always make sure you understand the why, how, and what-for. Otherwise, the help won't be very useful.
11. Always push your code to the develop branch only. The master branch will be ignored. Work inside the src directory.
12. Your directory should not contain any files besides those required for the tasks.

## Chapter II

### General Information

A **web application** is a type of client-server application in which the client interacts with a web server via a browser. The logic of a web application is distributed between the server and the client. Data storage primarily occurs on the server, and information exchange takes place over the network.

**Flask** is one of the most popular Python frameworks for creating web applications. Its advantages include:

- **Ease of use**: Flask has a simple and intuitive syntax, making it ideal for beginner developers or those who prefer clear, straightforward code.
- **Good documentation**: Flask offers well-structured, clear documentation that simplifies getting started and troubleshooting.
- **Flexibility**: Flask provides a flexible and modular approach to web development, allowing you to select the necessary components and features for your project.
- **Support for RESTful APIs**: Flask provides convenient tools for developing RESTful APIs, including routing, data serialization, and request/response handling.
- **Good integration with other tools**: Flask easily integrates with popular Python libraries and tools, such as SQLAlchemy for database work and Jinja2 for templating.

These advantages make Flask an attractive choice for developers aiming to build fast, scalable, and maintainable web applications in Python.

### Topics to Study

- Web application,
- Flask for the backend,
- API,
- Minimax algorithm,
- MVC.

## Chapter III

## Project: Tic-Tac-Toe
The project is created once and used for all subsequent tasks.

### Task 0. Project Setup

In order to develop in Python, you will need to install the appropriate interpreter. It can be downloaded from the official website. Once installed, you can use the command line and/or various integrated development environments (IDEs) to work on projects.  

In this context, a project is a set of .py files containing Python code that can be run individually via the command `python filename.py` (or `python3`) or imported into a file commonly named `main.py`.  

In PyCharm, creating a project is straightforward. You just select the Python interpreter to use and specify the save path and project name. You can also create a virtual environment, which is useful for large projects with many dependencies, such as libraries and frameworks.

### Task 1. Creating the Project Structure

- Each layer should be a separate module.
- The project structure must include the following layers: **web**, **domain**, **datasource**, and **di**.
- The **web** layer must contain the following packages for client interaction: model, module, route, and mapper.
- The **domain** layer must include the model and service packages to implement business logic.
- The **datasource** layer must include the model, repository, and mapper packages for data handling (e.g., database operations).
- The **di** layer contains configurations for dependency injection.

### Task 2. Implementing the Domain Layer

- Define the game board model as an integer matrix.
- Define the current game model, which includes a UUID and the game board.
- Define a service interface with the following methods:
  - A method to determine the next move in the current game using the Minimax algorithm.
  - A method to validate the current game board (checking that previous moves have not been altered).
  - A method to check if the game has ended.
- Place models, interfaces, and implementations in separate files.

### Task 3. Implementing the Datasource Layer

- Implement a storage class for current games.
- Use thread-safe collections for storage.
- Define models for the game board and the current game.
- Implement mappers between the domain and data source models (domain<->datasource).
- Implement a repository to work with the storage class that includes the following methods:
  - A method to save the current game.
  - A method to retrieve the current game.
- Create a class that implements the service interface and accepts the repository as a parameter to work with the storage class.
- Place models, interfaces, and implementations in separate files.

### Task 4. Implementing the Web Layer

- Define models for the game board and the current game.
- Implement mappers between the domain and web models (domain<->web).
- Implement a Flask controller with a POST method, /game/{current_game_UUID}, that accepts a current game with a user-updated game board and returns a current game with a computer-updated game board.
- If an invalid game with an updated board is sent, return an error with a description.
- Support multiple games running simultaneously.
- Models, interfaces, and implementations should be in separate files.

### Task 5. Implementing the DI Layer

- Implement a Container class that defines the dependency graph.
- It must include at least:
  - A singleton storage class.
  - A repository for working with the storage class.
  - A service for working with the repository.