const hour_card_1 = document.querySelector(".card-hour-1");
const hour_card_2 = document.querySelector(".card-hour-2");

const minute_card_1 = document.querySelector(".card-minute-1");
const minute_card_2 = document.querySelector(".card-minute-2");

const second_card_1 = document.querySelector(".card-second-1");
const second_card_2 = document.querySelector(".card-second-2");

// const endTime is already declared in home.html
const endDateTime = new Date(endTime);

const timer = () => {
    let now = new Date();

    console.log(endDateTime);

    console.log(now);

    // time left in milliseconds
    const timeLeft = Math.abs(endDateTime - now);
    let seconds = Math.floor(timeLeft / 1000);

    let hours = Math.floor(seconds / 3600);

    seconds = seconds % 3600;
    let minutes = Math.floor(seconds / 60);
    seconds = seconds % 60;

    console.log(hours, minutes, seconds);

    // make sure all are double digits
    // this assumes that max hours is 99
    hours = ("0" + hours.toString()).slice(-2);
    minutes = ("0" + minutes.toString()).slice(-2);
    seconds = ("0" + seconds.toString()).slice(-2);

    console.log(hours);

    // display time

    hour_card_1.textContent = hours[0];
    hour_card_2.textContent = hours[1];

    minute_card_1.textContent = minutes[0];
    minute_card_2.textContent = minutes[1];

    second_card_1.textContent = seconds[0];
    second_card_2.textContent = seconds[1];
};

setInterval(timer, 1000);
