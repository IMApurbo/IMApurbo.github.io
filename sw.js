/* Plain service worker, no backend/Firebase involved.
   loop.html calls registration.showNotification() directly whenever a message arrives while
   the browser is running (any tab state) — this file only needs to handle the notification
   being clicked, and route that back into the app. */

self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (event) => event.waitUntil(self.clients.claim()));

self.addEventListener("notificationclick", (event) => {
  const chatKey = (event.notification.data && event.notification.data.chatKey) || "";
  event.notification.close();

  event.waitUntil((async () => {
    const appUrl = new URL("./loop.html", self.registration.scope).href;
    const allClients = await clients.matchAll({ type: "window", includeUncontrolled: true });

    for(const client of allClients){
      if(client.url.startsWith(appUrl)){
        await client.focus();
        if(chatKey) client.postMessage({ type: "open-chat", chatKey });
        return;
      }
    }
    await clients.openWindow(chatKey ? `${appUrl}?chat=${encodeURIComponent(chatKey)}` : appUrl);
  })());
});
