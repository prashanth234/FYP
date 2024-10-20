export default function animateTitle(title: string) {
  const titleContainer = document.createElement('div');
  titleContainer.id = 'app-title-ani';
  titleContainer.className = 'logo';
  document.body.appendChild(titleContainer);

  let index = 0;

  const animate = () => {
      // Clear the current title content
      titleContainer.innerHTML = '';
      // Start with the opacity at 0
      titleContainer.style.opacity = '0';

      // Animate letter by letter
      const letterInterval = setInterval(() => {
          if (index < title.length) {
              titleContainer.innerHTML += title[index];
              index++;
          } else {
              clearInterval(letterInterval);
              index = 0; // Reset index for next loop

              // Fade out the title
              titleContainer.style.opacity = '0';
              setTimeout(() => {
                  // Fade in the title again
                  titleContainer.style.opacity = '1';
                  // Start the next animation cycle after a short delay
                  setTimeout(animate, 500); // Delay before the next loop
              }, 500); // Time for fade-out
          }

          titleContainer.style.opacity = '1';
      }, 200); // Delay for each letter
  };

  animate(); // Start the animation

  return titleContainer
}