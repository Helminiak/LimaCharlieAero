// Paint below-fold photos before a full-page capture. Decoding alone can leave
// asynchronous images blank in the compositor, even with a nonzero naturalWidth.
export async function prepareCapture(page) {
  await page.evaluate(async () => {
    const frames = () => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
    const images = [...document.images].filter(image => image.checkVisibility());
    for (const image of images) image.decoding = 'sync';
    await document.fonts.ready;
    for (let y = 0; y < document.documentElement.scrollHeight; y += innerHeight) {
      scrollTo(0, y);
      await frames();
    }
    await Promise.all(images.map(image => image.decode()));
    scrollTo(0, 0);
    await frames();
  });
}
