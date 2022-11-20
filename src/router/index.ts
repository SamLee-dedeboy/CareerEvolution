import { createRouter, createWebHistory } from "vue-router";
import Overview from "../views/Overview.vue";
import ActorView from "../views/ActorView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // {
    //   path: "/",
    //   name: "overview",
    //   component: Overview,
    // },
    {
      path: "/",
      name: "actorview",
      component: ActorView,
    },
  ],
});

export default router;
