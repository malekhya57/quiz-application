// Use relative URLs since session-based authentication is in place.
function loadQuizQuestions() {
    const quizContent = document.getElementById("quiz-content");
    if (!quizContent) return;
  
    fetch(`/quiz/get_random_questions`)
    .then(res => {
        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
        }
        return res.json();
    })
    .then(questions => {
        totalQuestions = questions.length; // Store the total questions loaded
        quizContent.innerHTML = "";
        if (questions.length > 0) {
            questions.forEach((q, index) => {
                const questionDiv = document.createElement("div");
                questionDiv.className = "mb-4";
                questionDiv.innerHTML = `
                  <h5>Question ${index + 1}: ${q.question_text}</h5>
                  <div>
                    ${Object.entries(q.options).map(([key, value]) => `
                      <div class="form-check">
                        <input class="form-check-input answer-input" type="radio" name="question-${q.id}" id="question-${q.id}-option-${key}" data-question-id="${q.id}" value="${key}">
                        <label class="form-check-label" for="question-${q.id}-option-${key}">
                          ${key}: ${value}
                        </label>
                      </div>
                    `).join('')}
                  </div>
                `;
                quizContent.appendChild(questionDiv);
            });
        } else {
            quizContent.innerHTML = "<p>No questions available at the moment.</p>";
        }
    })
    .catch(err => {
        console.error("Error loading quiz questions:", err);
        quizContent.innerHTML = "<p>Error loading questions. Please try again later.</p>";
    });
  }
  
  document.addEventListener("DOMContentLoaded", function() {
      if (document.getElementById("quiz-content")) {
          loadQuizQuestions();
      }
      if (document.getElementById("results-table")) {
          loadUserResults();
      }
  });
    
  function submitQuiz() {
    const answers = [];
    document.querySelectorAll('.answer-input').forEach(input => {
        if (input.checked) {
            answers.push({
                question_id: parseInt(input.dataset.questionId),
                selected_answer: input.value
            });
        }
    });
    
    if (answers.length < totalQuestions) {
        if (!confirm("You have not answered all questions. Do you want to submit anyway?")) {
            return;
        }
    }

    const payload = {
         answers: answers,
         total: totalQuestions
    };

    fetch(`/quiz/submit_quiz`, {
         method: "POST",
         headers: { 
             "Content-Type": "application/json"
         },
         body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(data => {
         alert("Quiz submitted! Your score: " + data.score + " out of " + data.total);
         // Redirect to the results page
         window.location.href = "/quiz/results";
    })
    .catch(err => console.error("Error submitting quiz:", err));
}

  
function loadUserResults() {
    fetch(`/quiz/results_data`)
        .then(res => {
            if (!res.ok) {
                throw new Error(`HTTP error! status: ${res.status}`);
            }
            return res.json();
        })
        .then(results => {
            const resultsTable = document.getElementById("results-table");
            resultsTable.innerHTML = "";
            results.forEach(result => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${result.id}</td>
                    <td>${result.score}</td>
                    <td>${result.total}</td>
                    <td>${result.timestamp}</td>
                `;
                resultsTable.appendChild(row);
            });
        })
        .catch(err => console.error("Error loading results:", err));
}


  document.addEventListener("DOMContentLoaded", function() {
    if (document.getElementById("results-table")) {
        loadUserResults();
    }
});

  
  // Admin functions
  
  function deleteQuestion(questionId) {
    if (confirm('Are you sure you want to delete this question?')) {
      fetch(`/admin/delete_question/${questionId}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json'
        }
      })
      .then(response => response.json())
      .then(result => {
        if (result.message === 'Question deleted successfully') {
          document.getElementById(`question-row-${questionId}`).remove();
          alert(result.message);
        } else {
          alert('Failed to delete question');
        }
      })
      .catch(error => {
        console.error('Error deleting question:', error);
        alert('An error occurred while deleting the question.');
      });
    }
  }
  
  function addQuestion() {
      const questionText = document.getElementById("new_question_text").value.trim();
      const optionA = document.getElementById("new_option_a").value.trim();
      const optionB = document.getElementById("new_option_b").value.trim();
      const optionC = document.getElementById("new_option_c").value.trim();
      const optionD = document.getElementById("new_option_d").value.trim();
      const correctAnswer = document.getElementById("new_correct_answer").value.trim().toUpperCase();
  
      if (!questionText || !optionA || !optionB || !optionC || !optionD || !correctAnswer) {
          alert("Please fill in all fields.");
          return;
      }
      if (!["A", "B", "C", "D"].includes(correctAnswer)) {
          alert("Correct answer must be A, B, C, or D.");
          return;
      }
  
      const data = {
          question_text: questionText,
          option_a: optionA,
          option_b: optionB,
          option_c: optionC,
          option_d: optionD,
          correct_answer: correctAnswer
      };
  
      fetch(`/admin/add_question`, {
          method: "POST",
          headers: { 
              "Content-Type": "application/json"
          },
          body: JSON.stringify(data)
      })
      .then(response => response.json())
      .then(result => {
          alert(result.message);
          if(result.message.toLowerCase().includes("success")) {
              location.reload(); 
          }
      })
      .catch(error => {
          console.error("Error adding question:", error);
          alert("There was an error adding the question.");
      });
  }

let totalQuestions = 0;
