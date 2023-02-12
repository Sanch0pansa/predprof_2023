<template>
  <div class="card">
    <div class="card-body">
      <h5 class="card-title">Общая информация</h5>
      <p class="card-text">
        <span class="badge bg-success" style="width: 30px"><i class="fas fa-check text-light"></i></span> {{ working }} работают <br>
        <span class="badge bg-warning" style="width: 30px"><i class="fas fa-signal text-light"></i></span> {{ lazy_loading }} работают медленно <br>
        <span class="badge bg-danger" style="width: 30px"><i class="fas fa-times text-light"></i></span> {{ not_working }} не работают <br>
      </p>
    </div>

    <EventsList :events="events"></EventsList>
  </div>
</template>

<script>
import {mapActions} from "vuex";
import EventsList from "@/components/items/EventsList.vue";

export default {
  name: "PageEvents",
  components: {EventsList},
  data() {
    return {
      working: 0,
      lazy_loading: 0,
      not_working: 0,
      events: [],
    }
  },
  methods: {
    ...mapActions({
      getEvents: "events/getEvents"
    }),

    async fetchEvents() {
      let data = await this.getEvents();

      this.working = data.working;
      this.lazy_loading = data.lazy_loading;
      this.not_working = data.not_working;
      this.events = data.events;
    }
  },

  async mounted() {
    await this.fetchEvents();
  }
}
</script>

<style scoped>

</style>