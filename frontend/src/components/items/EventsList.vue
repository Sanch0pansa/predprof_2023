<template>
  <ul class="list-group list-group-flush border-top">
    <EventsListItem :data="event" v-for="event in getEvents()"></EventsListItem>

    <li class="list-group-item card-body py-3" v-if="events.length > 3">
      <span class="text-primary" role="button" @click="() => {opened = !opened}">{{ opened ? "Свернуть" : `Развернуть (eщё ${events.length - 3})` }}</span>
    </li>
    <li class="list-group-item card-body py-3" v-if="events.length === 0"><span class="text-muted">Нет событий</span></li>
  </ul>
</template>

<script>
import EventsListItem from "@/components/items/EventsListItem.vue";

export default {
  name: "EventsList",
  components: {EventsListItem},
  props: {
    events: {
      required: true,
      type: Array,
    }
  },
  data() {
    return {
      opened: false,
    }
  },
  methods: {
    getEvents() {
      if (this.opened) {
        return this.events;
      } else {
        return this.events.slice(0, 3);
      }
    }
  }
}
</script>

<style scoped>

</style>