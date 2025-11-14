// Global variables
let currentQuiz = null;
let userAnswers = {};
let currentView = 'homepage';
let topicData = {};

// DOM ready handler
$(document).ready(function() {
    // Initial view
    renderHomepage();
    
    // Setup event listeners
    setupEventListeners();
    
    // Check for direct quiz access (e.g., from profile page)
    checkDirectQuizAccess();
});

function checkDirectQuizAccess() {
    // Check if URL has a quiz ID hash
    const hash = window.location.hash;
    if (hash && hash.length > 1) {
        const quizId = parseInt(hash.substring(1));
        if (!isNaN(quizId)) {
            loadQuizById(quizId);
        }
    }
}

function setupEventListeners() {
    // Content type switch (text/topic/file)
    $(document).on('change', 'input[name="contentType"]', function() {
        const contentType = $('input[name="contentType"]:checked').val();
        
        // Hide all sections first
        $('#textInputSection, #topicSelectSection, #fileUploadSection').addClass('d-none');
        
        // Show the appropriate section
        if (contentType === 'text') {
            $('#textInputSection').removeClass('d-none');
        } else if (contentType === 'topic') {
            $('#topicSelectSection').removeClass('d-none');
            loadTopicData();
        } else if (contentType === 'file') {
            $('#fileUploadSection').removeClass('d-none');
        }
    });
    
    // Topic and subtopic selection
    $(document).on('change', '#topicSelect', function() {
        const topic = $(this).val();
        updateTopicDescription(topic);
        populateSubtopics(topic);
    });
    
    // Upload document button
    $(document).on('click', '#uploadBtn', function() {
        uploadDocument();
    });
    
    // Generate quiz button
    $(document).on('click', '#generateBtn', function() {
        generateQuiz();
    });
    
    // Submit quiz button
    $(document).on('click', '#submitQuizBtn', function() {
        submitQuiz();
    });
    
    // New quiz buttons
    $(document).on('click', '#newQuizBtn, #newQuizFromResultsBtn', function() {
        renderHomepage();
    });
    
    // MCQ option selection
    $(document).on('click', '.option-item', function() {
        const questionId = $(this).closest('.question-container').data('id');
        const optionValue = $(this).data('value');
        
        // Update UI
        $(this).siblings().removeClass('selected');
        $(this).addClass('selected');
        
        // Store answer
        userAnswers[questionId] = optionValue;
    });
    
    // True/False selection
    $(document).on('change', '.true-false-radio', function() {
        const questionId = $(this).closest('.question-container').data('id');
        const value = $(this).val();
        
        // Store answer
        userAnswers[questionId] = value;
    });
    
    // Fill in the blank input
    $(document).on('input', '.fill-blank-input', function() {
        const questionId = $(this).closest('.question-container').data('id');
        const value = $(this).val();
        
        // Store answer
        userAnswers[questionId] = value;
    });
    
    // Number of questions adjusters
    $(document).on('click', '#increaseQuestions', function() {
        const input = $('#numQuestions');
        const currentValue = parseInt(input.val());
        if (currentValue < parseInt(input.attr('max'))) {
            input.val(currentValue + 1);
        }
    });
    
    $(document).on('click', '#decreaseQuestions', function() {
        const input = $('#numQuestions');
        const currentValue = parseInt(input.val());
        if (currentValue > parseInt(input.attr('min'))) {
            input.val(currentValue - 1);
        }
    });
    
    // About modal
    $(document).on('click', '#aboutLink', function(e) {
        e.preventDefault();
        $('#aboutModal').modal('show');
    });
}

function loadTopicData() {
    // Only fetch if we haven't already
    if (Object.keys(topicData).length === 0) {
        fetch('/api/topics')
            .then(response => response.json())
            .then(data => {
                topicData = data.topics;
                // Update UI if topic is already selected
                const selectedTopic = $('#topicSelect').val();
                if (selectedTopic) {
                    updateTopicDescription(selectedTopic);
                    populateSubtopics(selectedTopic);
                }
            })
            .catch(error => {
                console.error('Error loading topic data:', error);
            });
    }
}

function updateTopicDescription(topic) {
    if (!topic || !topicData[topic]) return;
    
    $('#topicTitle').text(topic);
    $('#topicDescription').text(topicData[topic].description);
}

function populateSubtopics(topic) {
    const subtopicSelect = $('#subtopicSelect');
    subtopicSelect.empty();
    subtopicSelect.append('<option value="" selected>All subtopics</option>');
    
    if (!topic || !topicData[topic]) {
        subtopicSelect.prop('disabled', true);
        return;
    }
    
    const subtopics = topicData[topic].subtopics;
    if (subtopics && subtopics.length > 0) {
        subtopics.forEach(subtopic => {
            subtopicSelect.append(`<option value="${subtopic}">${subtopic}</option>`);
        });
        subtopicSelect.prop('disabled', false);
    } else {
        subtopicSelect.prop('disabled', true);
    }
}

function renderHomepage() {
    // Reset global state
    currentQuiz = null;
    userAnswers = {};
    currentView = 'homepage';
    
    // Clear URL hash
    history.pushState("", document.title, window.location.pathname + window.location.search);
    
    // Load quiz history
    loadQuizHistory();
}

function loadQuizHistory() {
    // Show loading state
    $('#historyLoading').removeClass('d-none');
    $('#historyEmpty').addClass('d-none');
    
    // Fetch quiz history from API
    fetch('/api/quizzes')
        .then(response => response.json())
        .then(data => {
            // Hide loading state
            $('#historyLoading').addClass('d-none');
            
            const quizzes = data.quizzes || [];
            const historyList = $('#historyList');
            
            // Clear any existing content (except loading and empty states)
            historyList.find('.quiz-history-item').remove();
            
            if (quizzes.length === 0) {
                // Show empty state if no quizzes
                $('#historyEmpty').removeClass('d-none');
                return;
            }
            
            // Render each quiz in the history
            quizzes.forEach(quiz => {
                const date = new Date(quiz.created_at);
                const formattedDate = date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                
                const difficultyBadge = getDifficultyBadge(quiz.difficulty);
                
                const quizItem = `
                    <a href="#" class="list-group-item list-group-item-action quiz-history-item" data-id="${quiz.id}">
                        <div class="d-flex w-100 justify-content-between align-items-center">
                            <h5 class="mb-1">${quiz.title}</h5>
                            ${difficultyBadge}
                        </div>
                        <div class="d-flex justify-content-between align-items-center">
                            <small class="text-muted">${formattedDate}</small>
                            <span class="badge bg-secondary">${quiz.question_count} questions</span>
                        </div>
                    </a>
                `;
                
                historyList.prepend(quizItem);
            });
            
            // Add click event to load selected quiz
            $('.quiz-history-item').on('click', function(e) {
                e.preventDefault();
                const quizId = $(this).data('id');
                loadQuizById(quizId);
            });
        })
        .catch(error => {
            console.error('Error loading quiz history:', error);
            $('#historyLoading').addClass('d-none');
            $('#historyEmpty').removeClass('d-none')
                .html('<i class="bi bi-exclamation-circle text-danger" style="font-size: 2rem;"></i><p class="mt-2">Failed to load quiz history.</p>');
        });
}

function getDifficultyBadge(difficulty) {
    switch(difficulty) {
        case 'easy':
            return '<span class="badge bg-success">Easy</span>';
        case 'hard':
            return '<span class="badge bg-danger">Hard</span>';
        case 'medium':
        default:
            return '<span class="badge bg-warning">Medium</span>';
    }
}

function loadQuizById(quizId) {
    // Update URL hash for direct access
    window.location.hash = quizId;
    
    // Show loading state
    $('#app').html('<div class="d-flex justify-content-center mt-5"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div></div>');
    
    // Fetch quiz from API
    fetch(`/api/quiz/${quizId}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            
            // Render the quiz
            renderQuiz(data.quiz);
        })
        .catch(error => {
            console.error('Error loading quiz:', error);
            $('#app').html(`
                <div class="alert alert-danger mt-4" role="alert">
                    <h4 class="alert-heading">Error Loading Quiz</h4>
                    <p>Failed to load the requested quiz. Please try again.</p>
                    <hr>
                    <button class="btn btn-primary" onclick="renderHomepage()">
                        <i class="bi bi-arrow-left me-1"></i> Back to Home
                    </button>
                </div>
            `);
        });
}

function renderQuiz(quiz) {
    // Update global state
    currentQuiz = quiz;
    userAnswers = {};
    currentView = 'quiz';
    
    // Load template
    const template = $('#quiz-template').html();
    $('#app').html(template);
    
    // Set quiz title
    $('#quizTitle').text(quiz.title);
    
    // Render questions
    const questionsContainer = $('#quizQuestions');
    questionsContainer.empty();
    
    quiz.questions.forEach((question, index) => {
        const questionHtml = renderQuestion(question, index + 1);
        questionsContainer.append(questionHtml);
    });
}

function renderQuestion(question, number) {
    let html = `
        <div class="question-container" data-id="${question.id}" data-type="${question.type}">
            <div class="question-text">
                <span class="badge bg-primary me-2">${number}</span>
                ${question.text}
            </div>
    `;
    
    switch (question.type) {
        case 'mcq':
            html += renderMCQOptions(question);
            break;
        case 'true_false':
            html += renderTrueFalseOptions(question);
            break;
        case 'fill_blank':
            html += renderFillBlankInput(question);
            break;
        case 'math':
            html += renderFillBlankInput(question);
            break;
    }
    
    html += '</div>';
    return html;
}

function renderMCQOptions(question) {
    let html = '<ul class="question-options">';
    
    question.options.forEach((option, index) => {
        html += `
            <li class="option-item" data-value="${option}">
                <span class="option-letter">${String.fromCharCode(65 + index)}.</span>
                ${option}
            </li>
        `;
    });
    
    html += '</ul>';
    return html;
}

function renderTrueFalseOptions(question) {
    return `
        <div class="form-check">
            <input class="form-check-input true-false-radio" type="radio" 
                   name="tf-${question.id}" id="true-${question.id}" value="True">
            <label class="form-check-label" for="true-${question.id}">
                True
            </label>
        </div>
        <div class="form-check">
            <input class="form-check-input true-false-radio" type="radio" 
                   name="tf-${question.id}" id="false-${question.id}" value="False">
            <label class="form-check-label" for="false-${question.id}">
                False
            </label>
        </div>
    `;
}

function renderFillBlankInput(question) {
    return `
        <div class="fill-blank-container">
            <input type="text" class="fill-blank-input" 
                   placeholder="Type your answer..." autocomplete="off">
        </div>
    `;
}

function renderResults(results) {
    // Update global state
    currentView = 'results';
    
    // Load template
    const template = $('#results-template').html();
    $('#app').html(template);
    
    // Update score display
    $('#scorePercentage').text(`${Math.round(results.percentage)}%`);
    $('#scoreText').text(`You scored ${results.score} out of ${results.total}`);
    
    // Adjust score circle color based on percentage
    const scoreCircle = $('.score-circle');
    if (results.percentage < 40) {
        scoreCircle.css('background-color', 'var(--bs-danger)');
    } else if (results.percentage < 70) {
        scoreCircle.css('background-color', 'var(--bs-warning)');
    }
    
    // Render detailed results
    const resultsContainer = $('#resultsDetails');
    resultsContainer.empty();
    
    results.results.forEach((result, index) => {
        const question = currentQuiz.questions.find(q => q.id === result.question_id);
        const resultHtml = renderResultItem(question, result, index + 1);
        resultsContainer.append(resultHtml);
    });
}

function renderResultItem(question, result, number) {
    const resultClass = result.correct ? 'result-correct' : 'result-incorrect';
    const resultIcon = result.correct ? 
        '<i class="bi bi-check-circle-fill text-success me-2"></i>' : 
        '<i class="bi bi-x-circle-fill text-danger me-2"></i>';
    
    let html = `
        <div class="result-item ${resultClass}">
            <div class="result-header">
                ${resultIcon}
                <span class="badge bg-secondary me-2">${number}</span>
                ${question.text}
            </div>
            <div class="result-details mt-2">
    `;
    
    // Show different information based on question type
    switch (question.type) {
        case 'mcq':
            html += `
                <div>Your answer: ${result.user_answer || 'Not answered'}</div>
                <div>Correct answer: ${result.correct_answer}</div>
            `;
            break;
        case 'true_false':
            html += `
                <div>Your answer: ${result.user_answer || 'Not answered'}</div>
                <div>Correct answer: ${result.correct_answer}</div>
            `;
            break;
        case 'fill_blank':
            html += `
                <div>Your answer: ${result.user_answer || 'Not answered'}</div>
                <div>Correct answer: ${result.correct_answer}</div>
            `;
            break;
        case 'math':
            html += `
                <div>Your answer: ${result.user_answer || 'Not answered'}</div>
                <div>Correct answer: ${result.correct_answer}</div>
            `;
            break;
    }
    
    html += `
            </div>
        </div>
    `;
    
    return html;
}

function generateQuiz() {
    // Validate input
    const contentType = $('input[name="contentType"]:checked').val();
    let text = '';
    let topic = '';
    let subtopic = '';
    
    if (contentType === 'text') {
        text = $('#textInput').val().trim();
        if (!text) {
            alert('Please enter some text to generate a quiz.');
            return;
        }
    } else if (contentType === 'topic') {
        topic = $('#topicSelect').val();
        subtopic = $('#subtopicSelect').val();
        if (!topic) {
            alert('Please select a topic.');
            return;
        }
    } else if (contentType === 'file') {
        // Handled by the upload button
        alert('Please upload a file first.');
        return;
    }
    
    // Get question types
    const questionTypes = [];
    if ($('#typeMCQ').is(':checked')) questionTypes.push('mcq');
    if ($('#typeTF').is(':checked')) questionTypes.push('true_false');
    if ($('#typeFillBlank').is(':checked')) questionTypes.push('fill_blank');
    if ($('#typeMath').is(':checked')) questionTypes.push('math');
    
    if (questionTypes.length === 0) {
        alert('Please select at least one question type.');
        return;
    }
    
    // Get other settings
    const numQuestions = $('#numQuestions').val();
    const difficulty = $('#difficulty').val();
    
    // Show loading state
    $('#generateBtn').prop('disabled', true);
    $('#generationSpinner').removeClass('d-none');
    
    // Prepare request data
    const requestData = {
        contentType: contentType,
        text: text,
        topic: topic,
        subtopic: subtopic,
        numQuestions: numQuestions,
        difficulty: difficulty,
        questionTypes: questionTypes
    };
    
    // Send request to generate quiz
    fetch('/api/generate-quiz', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        // Reset UI
        $('#generateBtn').prop('disabled', false);
        $('#generationSpinner').addClass('d-none');
        
        if (data.error) {
            alert('Error: ' + data.error);
            return;
        }
        
        // Render the generated quiz
        renderQuiz(data.quiz);
    })
    .catch(error => {
        // Reset UI
        $('#generateBtn').prop('disabled', false);
        $('#generationSpinner').addClass('d-none');
        
        console.error('Error generating quiz:', error);
        alert('Failed to generate quiz. Please try again.');
    });
}

function uploadDocument() {
    const fileInput = $('#fileUpload')[0];
    if (!fileInput.files || fileInput.files.length === 0) {
        alert('Please select a file to upload.');
        return;
    }
    
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);
    
    // Show loading state
    $('#uploadBtn').prop('disabled', true);
    $('#uploadStatus').removeClass('d-none');
    $('#uploadStatusText').text('Processing document...');
    
    // Upload the file
    fetch('/api/upload-document', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Reset UI
        $('#uploadBtn').prop('disabled', false);
        
        if (data.error) {
            $('#uploadStatus').removeClass('d-none').html(`
                <div class="alert alert-danger">
                    <i class="bi bi-exclamation-circle me-2"></i>
                    ${data.error}
                </div>
            `);
            return;
        }
        
        // Show success and set the extracted text
        $('#uploadStatus').removeClass('d-none').html(`
            <div class="alert alert-success">
                <i class="bi bi-check-circle me-2"></i>
                Document processed successfully!
            </div>
        `);
        
        // Switch to text input mode and populate with extracted text
        $('input[name="contentType"][value="text"]').prop('checked', true).trigger('change');
        $('#textInput').val(data.text);
    })
    .catch(error => {
        // Reset UI
        $('#uploadBtn').prop('disabled', false);
        $('#uploadStatus').removeClass('d-none').html(`
            <div class="alert alert-danger">
                <i class="bi bi-exclamation-circle me-2"></i>
                Failed to process document. Please try again.
            </div>
        `);
        console.error('Error uploading document:', error);
    });
}

function submitQuiz() {
    if (!currentQuiz) return;
    
    // Check if user has answered all questions
    const answeredCount = Object.keys(userAnswers).length;
    const totalQuestions = currentQuiz.questions.length;
    
    if (answeredCount < totalQuestions) {
        const unansweredCount = totalQuestions - answeredCount;
        const confirmMsg = `You haven't answered ${unansweredCount} question(s). Do you want to submit anyway?`;
        
        if (!confirm(confirmMsg)) {
            return;
        }
    }
    
    // Prepare submission data
    const submissionData = {
        quizId: currentQuiz.id,
        answers: userAnswers
    };
    
    // Show loading state
    $('#submitQuizBtn').prop('disabled', true).html(`
        <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
        Submitting...
    `);
    
    // Submit the quiz
    fetch('/api/submit-quiz', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(submissionData)
    })
    .then(response => response.json())
    .then(data => {
        // Reset UI
        $('#submitQuizBtn').prop('disabled', false).html(`
            <i class="bi bi-check-circle me-1"></i> Submit Quiz
        `);
        
        if (data.error) {
            alert('Error: ' + data.error);
            return;
        }
        
        // Render the results
        renderResults(data);
    })
    .catch(error => {
        // Reset UI
        $('#submitQuizBtn').prop('disabled', false).html(`
            <i class="bi bi-check-circle me-1"></i> Submit Quiz
        `);
        
        console.error('Error submitting quiz:', error);
        alert('Failed to submit quiz. Please try again.');
    });
}
