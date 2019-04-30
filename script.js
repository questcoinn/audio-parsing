(() => {
  const lineChange = () => {
    const offHeight = document.documentElement.offsetHeight;
    const clientHeight = document.documentElement.clientHeight;
    const scroll = document.documentElement.scrollTop;

    const size = offHeight <= clientHeight ? 100 : scroll / (offHeight - clientHeight) * 100;
    document.querySelector(".line").style.width = `${size}%`
  }

  window.onscroll = lineChange;
  window.onload = lineChange;

  const getDeg = target => {
    const time = target.currentTime;
    const sec = Math.floor(time);
    return ((sec % 8) + (time - sec)) / 8 * 360;
  }

  const rotate = e => {
    const deg = getDeg(e.target);
    
    const style = e.target.parentNode.firstElementChild.style;

    style.transform = `rotate(${deg}deg)`;

    document.styleSheets[1].rules.item(0).cssRules[0].style.transform = `rotate(${deg}deg)`;
    document.styleSheets[1].rules.item(0).cssRules[1].style.transform = `rotate(${deg + 360}deg)`;
    
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

    document.styleSheets[1].rules.item(0).cssRules[0].style.transform = `rotate(${deg}deg)`;
    document.styleSheets[1].rules.item(0).cssRules[1].style.transform = `rotate(${deg + 360}deg)`;
  }

  const turnBack = e => {
    const deg = getDeg(e.target);
    
    const img   = e.target.parentNode.firstElementChild;
    const style = img.style;

    style.transform = `rotate(${deg}deg)`;
    
    style.animationName = "turn-back";
    style.animationDuration = "1s";
    style.animationIterationCount = "";
    style.animationTimingFunction = "";

    document.styleSheets[1].rules.item(0).cssRules[0].style.transform = "rotate(0deg)";
    document.styleSheets[1].rules.item(0).cssRules[1].style.transform = "rotate(360deg)";

    img.addEventListener("animationend", () => {
      style.transform = "rotate(0deg)";
    });
  }

  for(let node of document.querySelectorAll(".load")) {
    node.addEventListener("click", e => {
      const btn = e.target;

      const audioNode = document.createElement("audio");
      audioNode.setAttribute("src", btn.src);
      audioNode.setAttribute("controls", "controls");
      if(btn.getAttribute("download") === "0") {
        audioNode.setAttribute("controlsList", "nodownload");
      }
      
      btn.parentNode.replaceChild(audioNode, e.target);

      audioNode.addEventListener('contextmenu', e => e.preventDefault());
      audioNode.addEventListener('canplay', e => {
        e.target.addEventListener('play', rotate);
        e.target.addEventListener('pause', goto);
        e.target.addEventListener('ended', turnBack);
      });
    });
  }
})()