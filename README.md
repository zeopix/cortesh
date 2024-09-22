# 🧠 **Cortesh** — COgnitive Real-Time Software Helper ⚡

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg) ![CLI](https://img.shields.io/badge/cli-automation-brightgreen.svg) ![Langchain](https://img.shields.io/badge/langchain-powered-ff69b4.svg) ![OpenAI](https://img.shields.io/badge/OpenAI-api-orange.svg)

## **Introduction** 🎯

**cortesh** is a LLM based CLI tool that interacts with your coding project. It aims to:
- 🚀 Quickly bootstrap new software projects.
- 📂 Generate embeddings and/or custom trainings for your existing projects.
- 📑 Implement features and functionalities.
- ⚡ Create and run tests.
- 🐞Debug and fix bugs. 
- 🔒Automatic security and performance analysis.

## **Demo** 📺

[![Cortesh Demo](https://img.youtube.com/vi/EZqdUPMIz0k/0.jpg)](https://www.youtube.com/watch?v=EZqdUPMIz0k)


---

## **Roadmap** ✨
- [x] Initialize with OpenAI.
- [x] [ Logic ] - folder_project - entry point to handle user requests on a folder project.
- [x] [ Output ] Write files and run commands from LLM answers.
- [x] [ Logic ] Feedback loop for command outputs. Flow control. 
- [x] [ Sense ] Read current files and project structure, flow control by LLM.
- [ ] [ Memory ] Generate embeddings on curent project structure, include GIT/LLM generated descriptions.
- [ ] [ Logic ] Use the memory embedidngs in flow control
- [ ] Some kind of testing...



## **Installation** 🛠️

```bash
pip install cortesh
```

## **GOAL** 🎯
To be able to fully implement a feature on a public repository in a completely autonomous way.


## **Inspiration and Bibliography** 🌟
- [Code Generation with AlphaCodium](https://arxiv.org/abs/2401.08500)
- [Many-Shot In-Context learning](https://arxiv.org/pdf/2404.11018)
- [Chain of Agents: Large Language Models Collaborating on Long-Context Tasks](https://arxiv.org/abs/2406.02818)


---

## **Usage** 💻

Run the command in any project folder to instantly generate the structure and start using AI-powered commands.

```bash
fulcon --generate
```

### Example

```bash
$ fulcon
🌟 Good day there! What can I help you with today?
🗣 I want to create a todo webapp.

🌟 Sure thing! How does this sound?
  🚀React redux webapp.   
🗣 Sounds good!

📁 Creating directory: /todo-web-app
📁 Adding dependency: express body-parser
📁 Adding dependency: nodemon

📄 Writing app.js
📁 Creating directory: /todo-web-app/views
📁 Creating directory: /todo-web-app/public
📄 Writing public/style.css
🎉 Done! Your project is ready to go!
```

## **Documentation** 📚

### Command Line Options

| Command             | Description                                      |
|---------------------|--------------------------------------------------|
| `fulcon --generate` | Generates the folder and essential project files |
| `fulcon --reset`    | Resets the memory for the current project.       |
| `fulcon --version`  | Displays the current version of the tool         |

For more detailed documentation, head over to the [full docs](#) (link to be added).

---

## **Contributing** 🤝

We welcome contributions! Here's how you can help:

1. Fork the repository 🍴
2. Create your feature branch (`git checkout -b feature/your-feature`) 🌱
3. Commit your changes (`git commit -am 'Add some feature'`) 💡
4. Push to the branch (`git push origin feature/your-feature`) 🚀
5. Open a Pull Request ✨

Check the [Contributing Guidelines](#) for more information.

---

## **License** 📜

This project is licensed under the **MIT License**. See the [LICENSE](./LICENSE) file for details.

---

**Happy Coding!** ✨