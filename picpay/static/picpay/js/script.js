const target = {
    clicked: 0,
    currentFollowers: 90,
    btn: document.querySelector("a.btn"),
    fw: document.querySelector("span.followers")
};

const follow = () => {
    target.clicked += 1;
    target.btn.innerHTML = 'Following <i class="fas fa-user-times"></i>';

    if (target.clicked % 2 === 0) {
        target.currentFollowers -= 1;
        target.btn.innerHTML = 'Follow <i class="fas fa-user-plus"></i>';
    }
    else {
        target.currentFollowers += 1;
    }

    target.fw.textContent = target.currentFollowers;
    target.btn.classList.toggle("following");
}


const transactionTab = document.getElementById("transactionTab")

function toggleTab(tab) {

    if (tab == 'transaction') {
        if (transactionTab.style.left === "0px") {
            transactionTab.style.left = "-100%";

        } else {
            transactionTab.style.left = "0px";
        }
    }



}