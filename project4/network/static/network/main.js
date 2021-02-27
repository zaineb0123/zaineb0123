
//When page loads, and the button shows "Following", style the button differently
function loadJS() {
    console.log("i am running in loadJS");
    var btnText = document.querySelector('#followBtn').textContent;
    if (btnText == 'Following') {
        document.querySelector("#followBtn").style.setProperty('--hover-color', 'crimson');
        document.querySelector("#followBtn").addEventListener("mouseover", function () {
            this.textContent = "Unfollow";
        });
        document.querySelector("#followBtn").addEventListener("mouseout", function () {
            this.textContent = "Following";
        });
       

    } else {
        document.querySelector("#followBtn").style.setProperty('--hover-color', ' #007bff');
    }
}

//style the button after the it has been clicked
function followClick() {
    // var btnText = document.querySelector('#followBtn').textContent;
    // if (btnText == 'Follow') {
    //     document.querySelector('#followBtn').textContent = 'Following';
    //     document.querySelector("#followBtn").style.setProperty('--hover-color', 'crimson')

    //     document.querySelector("#followBtn").addEventListener("mouseover", function () {
    //         this.textContent = "Unfollow";
    //     });
    //     document.querySelector("#followBtn").addEventListener("mouseout", function () {
    //         this.textContent = "Following";
    //     });

    // } else {
    //     document.querySelector('#followBtn').textContent = 'Follow';
    //     document.querySelector("#followBtn").style.setProperty('--hover-color', ' #007bff')

    //     document.querySelector("#followBtn").addEventListener("mouseover", function () {
    //         this.textContent = "Follow";
    //     });
    //     document.querySelector("#followBtn").addEventListener("mouseout", function () {
    //         this.textContent = "Follow";
    //     });
    // }
}



//load modal for Editing
function loadModal(id) {
    //load the modal
    var modal = document.getElementById("myModal");
    var btn = document.getElementById("editLink");
    var span = document.getElementsByClassName("close")[0];
    var saveBtn = document.getElementById("saveButton");



    //populate the modal with tweet content
    fetch(`/edit/${id}`)
    .then(response => response.json())
    .then(postDetails => {
       
        modal.style.display = "block";
        postDetails.forEach(element => { 
            document.querySelector('#editPostBox').value = `${element.postContent}`;
    })

    })
   
   
    // When the user clicks on <span> (x), close the modal
    span.onclick = function () {
        modal.style.display = "none";
    }

    saveBtn.onclick = function(){
        const updatedValue = document.querySelector('#editPostBox').value
        fetch(`/edit/${id}`, {
            method: 'PUT',
            body: JSON.stringify({
              postContent: updatedValue
            })
        }).then(response=> {
            //if update succeeds in backend
            const updateCard = document.querySelector('#cardID');
            const children = updateCard.children; // find all children elements 
            for(let i = 0; i < children.length; i++)
            {
                if(children[i].id === 'contents')  // find contents of p tag 
                {
                    console.log("inside contents")
                    children[i].innerText = updatedValue; // change inner text of p tag
                    return;
                }
            }
        })
    
        modal.style.display = "none";
    }



    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
}


function likeOnClick(ele, id) {
    var postId;
    postId = id;
    console.log("I went inside the function", postId);
    count = document.querySelector(`#like_count-${id}`);
    console.log("value of count is ", count)
    
    var currentClass = $(ele).attr('class');
    if (currentClass == 'fa fa-thumbs-up')
    {
        console.log("dislike");
     $(ele).removeClass("fa fa-thumbs-up");   
        $(ele).addClass("fa fa-thumbs-down");
    }
    else{
        console.log("Like button");
        $(ele).removeClass("fa fa-thumbs-down");   
        $(ele).addClass("fa fa-thumbs-up");
    }   

    fetch(`/like_post/${id}`)
    .then(response=> response.json())
    .then(updateCount => {
        count.textContent = updateCount[0].likes
    });
   };


  