styleVal = '''@import url('https://fonts.googleapis.com/css?family=Dosis');
@keyframes rotate {
  0% { transform: rotate(0deg) }
  100% { transform: rotate(360deg) }
}
@keyframes turn-back {
  100% { transform: rotate(0deg) }
}
body {
  font-family: 'Dosis', sans-serif;
  background-color: #bbb;
  margin: 0;
}
header {
  background-color: #fff;
  height: 6.5rem;
  max-height: 6.5rem; 
  min-height: 6.5rem;
  width: 100%;
  text-align: center;
  box-shadow: 0px 4px 20px;
  z-index: 999;
  position: fixed;
  top: 0;
}
header p {
  margin: 0;
  font-size: 5rem;
}
.line {
  position: fixed;
  top: 6.3rem;
  border: 2px solid red;
  z-index: 1000;
}
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #fff;
  margin: 0 auto;
  width: 80%;
  padding-top: 8rem;
}
img {
  width: 200px;
  border-radius: 100px;
}
.item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px;
  margin-bottom: 20px;
  box-shadow: 0px 0px 20px;
  border-radius: 5px;
}
.title {
  margin: 5px 0;
  background-color: aliceblue;
}'''

scriptVal = '''lineChange = () => {
  const offHeight = document.documentElement.offsetHeight;
  const clientHeight = document.documentElement.clientHeight;
  const scroll = document.documentElement.scrollTop;

  const size = offHeight <= clientHeight ? 100 : scroll / (offHeight - clientHeight) * 100;
  document.querySelector(".line").style.width = `${size}%`
}
window.onscroll = lineChange
window.onload = lineChange

const getDeg = target => {
  const time = target.currentTime;
  const sec = Math.floor(time);
  return ((sec % 8) + (time - sec)) / 8 * 360;
}

const rotate = e => {
  const deg = getDeg(e.target);
  
  const style = e.target.parentNode.firstElementChild.style;

  style.transform = `rotate(${deg}deg)`;

  document.styleSheets[0].rules.item(1).cssRules[0].style.transform = `rotate(${deg}deg)`;
  document.styleSheets[0].rules.item(1).cssRules[1].style.transform = `rotate(${deg + 360}deg)`;
  
  style.animationName = "rotate";
  style.animationDuration = "8s";
  style.animationIterationCount = "infinite";
  style.animationTimingFunction = "linear";
}

const goto = e => {
  const deg = getDeg(e.target);
  
  const style = e.target.parentNode.firstElementChild.style;

  style.transform = `rotate(${deg}deg)`;
  
  style.animationName = "";
  style.animationDuration = "";
  style.animationIterationCount = "";
  style.animationTimingFunction = "";

  document.styleSheets[0].rules.item(1).cssRules[0].style.transform = `rotate(${deg}deg)`;
  document.styleSheets[0].rules.item(1).cssRules[1].style.transform = `rotate(${deg + 360}deg)`;
}

const turnBack = e => {
  const deg = getDeg(e.target);
  
  const style = e.target.parentNode.firstElementChild.style;

  style.transform = `rotate(${deg}deg)`;
  
  style.animationName = "turn-back";
  style.animationDuration = "1s";
  style.animationIterationCount = "";
  style.animationTimingFunction = "";

  document.styleSheets[0].rules.item(1).cssRules[0].style.transform = "rotate(0deg)";
  document.styleSheets[0].rules.item(1).cssRules[1].style.transform = "rotate(360deg)";

  setTimeout(() => style.transform = "rotate(0deg)", 1000);
}

for(let node of document.querySelectorAll("audio")) {
  node.addEventListener('contextmenu', e => e.preventDefault());
  node.addEventListener('canplay', e => {
    e.target.addEventListener('play', rotate);
    e.target.addEventListener('pause', goto);
    e.target.addEventListener('ended', turnBack);
  });
}'''
