$(function() {

  // Use buttons to toggle between views
  $('#inbox').on('click', () => load_mailbox('inbox'));
  $('#sent').on('click', () => load_mailbox('sent'));
  $('#archived').on('click', () => load_mailbox('archive'));
  $('#compose').on('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  $('#emails-view').hide();
  $('#email').hide();
  $('#compose-view').show();

  // Clear out composition fields
  $('#compose-recipients').val('');
  $('#compose-subject').val('');
  $('#compose-body').val('');
}

let root = ReactDOM.createRoot(
  document.getElementById("emails-view")
);

let root1 = ReactDOM.createRoot(
  document.getElementById("email")
);

async function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  $('#emails-view').show();
  $('#compose-view').hide();
  $('#email').hide();

  // Show the mailbox name
  $('#emails-view').html(`<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`);

  //Load a mailbox on backend
  await fetch(`mailbox/${mailbox}`)
  .then( response => response.json())
  .then(data =>  {


    //Need a way to dynamically create divs    
    
    
    
      function Create_Div() {
        
        //Likely class needs to be set depending on response
        //Can be separated using for loop 
        //for each item, if item.read == true then store into one list if not other list then combine
        // ()=> is a thunk, aka it only gets called when value is needed vs func_read() which calls it now
        data = data.map(email => 
          <div>
            <div className={email.read ? "read" : "unread"} onClick={() => func0(email.id)} id={email.id}> 
              <p>From: {email.sender} Sub: {email.recipients} | | {email.body.substring(0, 20)}</p>
            </div>
            <button id="btn1" onClick={() => func_archive(email.id)}>Archive</button>
          </div>

   
         );

        

          return (
            <div>
              {data}  
            </div>

          );
      }
  
    root.render(<Create_Div/>);
    });

  //De-archives and changes read class
  function func_archive(id) {
    if (mailbox == "archive") {
      fetch(`/email/${id}`, {
        method: "PUT",
        body: JSON.stringify({
          archived: false
        })
      })
    }
    else {
      fetch(`/email/${id}`, {
      
        method: "PUT",
        body: JSON.stringify({ 
          archived: true
        })
      })
    }
    root.render(<Create_Div/>);
}

  }

//Load up a single email
function func0(id) {

  $('#emails-view').hide();
  $('#compose-view').hide();
  $('#email').show()
  
 

  fetch(`/email/${id}`)
  .then(response => response.json())
  .then(data => {
    //Need a way to dynamically create divs    
   
    
      function Create_Email() {

          return (
            <div className="read">
              <p>Sender: {data.sender}</p>
              <p>Recipient: {data.recipients} </p> 
              <p>Subject: {data.subject} </p> 
              <p>{data.body} </p>
              <p>{data.timestamp}</p> 
              <button id="btn0" onClick={() => func1(data.sender, data.subject, data.timestamp, data.body)}>Reply</button>
            </div>

          );
      }

    
    root1.render(<Create_Email/>);

  
  })

  
}

//prefill compose form
function func1(sender, subject, timestamp, body) {
  $('#compose-recipients').val(sender);
  $('#compose-subject').val(subject);
  $('#compose-body').val("ON" + timestamp + sender + "wrote:" + body );
  $('#emails-view').hide();
  $('#compose-view').show();
  $('#email').hide()
  
}

//Sending an email
$("#compose-form").on("submit", () => {
  fetch('compose', {
    method: 'POST',
    body: JSON.stringify({
        recipients: $("#compose-recipients").val(),
        subject: $("#compose-subject").val(),
        body: $("#compose-body").val(),
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
  });

  //Once sent load sent mailbox
  $('#compose-view').hide();
  $('#emails-view').show();
  

});



