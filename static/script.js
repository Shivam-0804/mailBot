// const socket = io.connect("http://" + document.domain + ":" + location.port);

// socket.on("new_emails", function ({ emails, summaries }) {
//   updateList(emails);
//   updateSummaryList(summaries);
// });

async function loadInbox() {
  const emailListContainer = document.getElementById("email-list");
  emailListContainer.innerHTML = "";
  emailListContainer.innerHTML += "<h2>Inbox</h2>";
  fetch("/inbox")
    .then((response) => response.json())
    .then((emails) => {
      updateList(emails);
    })
    .catch((error) => {
      console.error("Error fetching inbox emails:", error);
    });
}

function updateList(emails) {
  const emailListContainer = document.getElementById("email-list");
  emailListContainer.innerHTML = "";
  emailListContainer.innerHTML += "<h2>Inbox</h2>";
  if (emails.length === 0) {
    emailListContainer.innerHTML = "<p>No unread emails found.</p>";
    return;
  }

  emails.forEach((email) => {
    const emailHTML = `
      <div class="email-item">
        <span class="email-sender">${email.sender}</span>
        <span class="email-subject">${email.subject}</span>
        <span class="email-body">${email.body}</span>
      </div>
    `;
    emailListContainer.innerHTML += emailHTML;
  });
}

async function loadSummary() {
  const summaryListContainer = document.getElementById("email-list");
  summaryListContainer.innerHTML = "";
  summaryListContainer.innerHTML += "<h2>Summary</h2>";
  fetch("/summary")
    .then((response) => response.json())
    .then((data) => {
      updateSummaryList(data);
    })
    .catch((error) => {
      console.error("Error fetching email summaries:", error);
    });
}

function updateSummaryList(summaries) {
  const summaryListContainer = document.getElementById("email-list");
  summaryListContainer.innerHTML = "";
  summaryListContainer.innerHTML += "<h2>Summary</h2>";
  if (summaries.length === 0) {
    summaryListContainer.innerHTML = "<p>No summaries available.</p>";
    return;
  }

  summaries.forEach((summary) => {
    const summaryHTML = `
      <div class="email-item">
        <span class="email-sender">${summary.from}</span>
        <span class="email-subject">${summary.subject}</span>
        <span class="email-body">${summary.summary}...</span>
      </div>
    `;
    summaryListContainer.innerHTML += summaryHTML;
  });
}

async function loadTasks() {
  const taskListContainer = document.getElementById("email-list");
  taskListContainer.innerHTML = "";
  taskListContainer.innerHTML += "<h2>Tasks</h2>";
  fetch("/tasks")
    .then((response) => response.json())
    .then((data) => {
      updateTaskList(data);
    })
    .catch((error) => {
      console.error("Error fetching tasks:", error);
    });
}

function updateTaskList(tasks) {
  const taskListContainer = document.getElementById("email-list");
  taskListContainer.innerHTML = "";
  taskListContainer.innerHTML += "<h2>Tasks</h2>";

  if (tasks.length === 0) {
    taskListContainer.innerHTML = "<p>No tasks available.</p>";
    return;
  }

  tasks.forEach((task) => {
    const taskHTML = `
      <div class="email-item">
        <span class="email-sender">${task.title}</span>
        <span class="email-subject">${
          task.due ? new Date(task.due).toLocaleString() : "No due date"
        }</span>
      </div>
    `;
    taskListContainer.innerHTML += taskHTML;
  });
}

function filterEmails() {
  const filter = document.getElementById("search-bar").value.toLowerCase();
  const emails = document.querySelectorAll(".email-item");

  emails.forEach((email) => {
    const sender = email
      .querySelector(".email-sender")
      .textContent.toLowerCase();
    const subject = email
      .querySelector(".email-subject")
      .textContent.toLowerCase();

    if (sender.includes(filter) || subject.includes(filter)) {
      email.style.display = "";
    } else {
      email.style.display = "none";
    }
  });
}

function openComposeModal() {
  document.getElementById("compose-modal").style.display = "flex";
}

function closeComposeModal() {
  document.getElementById("compose-modal").style.display = "none";
}

function sendEmail() {
  var to = document.getElementById("to-email").value;
  var subject = document.getElementById("subject").value;
  var body = document.getElementById("body").value;

  if (to && subject && body) {
    alert("Email sent successfully to " + to);
    closeComposeModal();
  } else {
    alert("Please fill out all fields before sending!");
  }
}

const commands = [
  "/send-email",
  "/search",
  "/archive",
  "/delete",
  "/mark-read",
  "/flag",
  "/spam",
  "/help",
];

const commandInput = document.getElementById("command-line");
const suggestionsList = document.getElementById("suggestions");

commandInput.addEventListener("input", function (event) {
  const query = commandInput.value;

  if (query.startsWith("/")) {
    const searchTerm = query.slice(1).toLowerCase();
    const filteredCommands = commands.filter((command) =>
      command.toLowerCase().includes(searchTerm)
    );

    if (filteredCommands.length > 0) {
      suggestionsList.innerHTML = filteredCommands
        .map(
          (command) =>
            `<li onclick="selectCommand('${command}')">${command}</li>`
        )
        .join("");
      suggestionsList.style.display = "block";
    } else {
      suggestionsList.style.display = "none";
    }
  } else {
    suggestionsList.style.display = "none";
  }
});

function selectCommand(command) {
  commandInput.value = command;
  suggestionsList.style.display = "none";
}

function sendCommand() {
  const command = commandInput.value;
  if (command) {
    alert("Command executed: " + command);
  }
  commandInput.value = "";
}

function logout() {
  fetch("/logout", { method: "POST" })
    .then((response) => {
      if (response.ok) {
        window.location.reload();
      } else {
        console.error("Error logging out");
      }
    })
    .catch((error) => {
      console.error("Error logging out:", error);
    });
}

function openComposeModal() {
  document.getElementById("compose-modal").style.display = "block";
}

function closeComposeModal() {
  document.getElementById("compose-modal").style.display = "none";
}

function sendEmail() {
  const toEmail = document.getElementById("to-email").value;
  const subject = document.getElementById("subject").value;
  const body = document.getElementById("body").value;

  const emailData = {
    toEmail: toEmail,
    subject: subject,
    body: body,
  };

  fetch("/send_email", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(emailData),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        alert("Email sent successfully!");
        closeComposeModal();
      } else {
        alert("Error sending email: " + data.error);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("There was an error sending your email.");
    });
}
