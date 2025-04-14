// Function to fetch all books from the API
async function fetchAllBooks() {
  try {
    // Make a GET request to the API endpoint
    const response = await fetch("http://127.0.0.1:5000/api/books");

    // Check if the response status is OK (status code 200-299)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    // Parse the JSON response
    const books = await response.json();

    // Log the books to the console or process them as needed
    return books;
  } catch (error) {
    // Handle any errors that occur during the fetch
    console.error("Failed to fetch books:", error);
  }
}

window.onload = async function () {
  const books = await fetchAllBooks();
  const bookTable = document.querySelector("#book-table");
  for (let i = 0; i < books.length; i++) {
    const book = books[i];
    const id = book["book_id"];
    const title = book["book_title"];
    const authorName = book["author_name"];
    const publisherName = book["publisher_name"];
    const genreName = book["genre_name"];

    // Create table row for each book
    const row = document.createElement("tr");
    row.setAttribute("data-id", id);

    // Check if book is borrowed
    // const isBorrowed = borrowingData[id] ? true : false;

    // Populate row with book details, including genre
    // <td>${
    //   isBorrowed ? borrowingData[id].borrowerName : ""
    // }</td>
    // <td>${isBorrowed ? borrowingData[id].borrowDate : ""}</td>
    // <td>${isBorrowed ? borrowingData[id].returnDate : ""}</td>
    // <td>${isBorrowed ? "Borrowed" : "Present"}</td>
    row.innerHTML = `<td>${id}</td>
                     <td><a href="#" target="_blank">${title}</a></td>
                     <td><a href="#" target="_blank">${authorName}</a></td>
                     <td><a href="#" target="_blank">${publisherName}</a></td>
                     <td><a href="#" target="_blank">${genreName}</a></td>
                     `;
    bookTable.appendChild(row);

    // // Populate the appropriate dropdown
    // if (!isBorrowed) {
    //   // Add book to Borrow dropdown
    //   const option = document.createElement("option");
    //   option.value = id;
    //   option.textContent = `${id} - ${title}`;
    //   borrowBookSelect.appendChild(option);
    // } else {
    //   // Add book to Return dropdown
    //   const returnOption = document.createElement("option");
    //   returnOption.value = id;
    //   returnOption.textContent = `${id} - ${title}`;
    //   returnBookSelect.appendChild(returnOption);
    // }
  }
};

//         // Retrieve borrowing data from LocalStorage
//         const borrowingData = JSON.parse(localStorage.getItem('borrowingData')) || {};

//         // Clear existing options
//         borrowBookSelect.innerHTML = '<option value="">Select a Book</option>';
//         returnBookSelect.innerHTML = '<option value="">Select a Book</option>';

//     }).catch(error => {
//         console.error('Error fetching or parsing XML files:', error);
//     });
// };

// // Handle Borrow Form Submission
// document.getElementById('borrowForm').addEventListener('submit', function (event) {
//     event.preventDefault();
//     const bookId = document.getElementById('borrowBookId').value;
//     const borrowerName = document.getElementById('borrowerName').value.trim();
//     const borrowDate = document.getElementById('borrowDate').value;

//     if (!bookId || !borrowerName || !borrowDate) {
//         alert('Please fill in all fields.');
//         return;
//     }

//     // Confirmation Dialog
//     if (!confirm(`Are you sure you want to borrow Book ID ${bookId}?`)) {
//         return;
//     }

//     const row = document.querySelector(`#book-table tr[data-id="${bookId}"]`);
//     if (row) {
//         const currentState = row.cells[8].textContent;
//         if (currentState === 'Borrowed') {
//             alert('This book is already borrowed.');
//             return;
//         }

//         const returnDate = new Date(borrowDate);
//         returnDate.setMonth(returnDate.getMonth() + 3); // Set the return date 3 months later

//         // Update the table
//         row.cells[5].textContent = borrowerName;
//         row.cells[6].textContent = borrowDate;
//         row.cells[7].textContent = returnDate.toISOString().split('T')[0]; // Format the date as YYYY-MM-DD
//         row.cells[8].textContent = 'Borrowed';
//         row.classList.add('borrowed');

//         // Save borrowing details to LocalStorage
//         const borrowingData = JSON.parse(localStorage.getItem('borrowingData')) || {};
//         borrowingData[bookId] = {
//             borrowerName: borrowerName,
//             borrowDate: borrowDate,
//             returnDate: returnDate.toISOString().split('T')[0]
//         };
//         localStorage.setItem('borrowingData', JSON.stringify(borrowingData));

//         // Remove the borrowed book from Borrow Form dropdown
//         const borrowBookSelect = document.getElementById('borrowBookId');
//         const optionToRemove = borrowBookSelect.querySelector(`option[value="${bookId}"]`);
//         if (optionToRemove) {
//             optionToRemove.remove();
//         }

//         // Add the borrowed book to Return Form dropdown
//         const returnBookSelect = document.getElementById('returnBookId');
//         const newReturnOption = document.createElement('option');
//         newReturnOption.value = bookId;
//         newReturnOption.textContent = `${bookId} - ${row.cells[1].textContent}`;
//         returnBookSelect.appendChild(newReturnOption);

//         // Clear the form
//         document.getElementById('borrowForm').reset();

//         alert(`Book ID ${bookId} has been successfully borrowed.`);
//     } else {
//         alert('No book found with that ID.');
//     }
// });

// // Handle Return Form Submission
// document.getElementById('returnForm').addEventListener('submit', function (event) {
//     event.preventDefault();
//     const bookId = document.getElementById('returnBookId').value;
//     const returnDateInput = document.getElementById('returnDate').value;

//     if (!bookId || !returnDateInput) {
//         alert('Please fill in all fields.');
//         return;
//     }

//     // Confirmation Dialog
//     if (!confirm(`Are you sure you want to return Book ID ${bookId}?`)) {
//         return;
//     }

//     const row = document.querySelector(`#book-table tr[data-id="${bookId}"]`);
//     if (row) {
//         const currentState = row.cells[8].textContent;
//         if (currentState !== 'Borrowed') {
//             alert('This book is not currently borrowed.');
//             return;
//         }

//         // Update the table to clear borrowing details
//         row.cells[5].textContent = '';
//         row.cells[6].textContent = '';
//         row.cells[7].textContent = '';
//         row.cells[8].textContent = 'Present';
//         row.classList.remove('borrowed');

//         // Update LocalStorage
//         const borrowingData = JSON.parse(localStorage.getItem('borrowingData')) || {};
//         if (borrowingData[bookId]) {
//             borrowingData[bookId].returnDate = returnDateInput; // Optionally update the return date
//             // Remove the entry to indicate the book is returned
//             delete borrowingData[bookId];
//             localStorage.setItem('borrowingData', JSON.stringify(borrowingData));
//         }

//         // Remove the returned book from Return Form dropdown
//         const returnBookSelect = document.getElementById('returnBookId');
//         const optionToRemove = returnBookSelect.querySelector(`option[value="${bookId}"]`);
//         if (optionToRemove) {
//             optionToRemove.remove();
//         }

//         // Add the returned book back to Borrow Form dropdown
//         const borrowBookSelect = document.getElementById('borrowBookId');
//         const newBorrowOption = document.createElement('option');
//         newBorrowOption.value = bookId;
//         newBorrowOption.textContent = `${bookId} - ${row.cells[1].textContent}`;
//         borrowBookSelect.appendChild(newBorrowOption);

//         // Clear the form
//         document.getElementById('returnForm').reset();

//         alert(`Book ID ${bookId} has been successfully returned.`);
//     } else {
//         alert('No book found with that ID.');
//     }
// });

// // Clear borrowing data from localStorage
// document.getElementById('clearDataBtn').addEventListener('click', function () {
//     if (confirm('Are you sure you want to clear all borrowing data? This action cannot be undone.')) {
//         localStorage.removeItem('borrowingData'); // Only remove borrowing data
//         location.reload(); // Reload the page after clearing the data
//     }
// });
