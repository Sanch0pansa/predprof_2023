<template>
  <ul class="nav nav-pills">
    <li class="nav-item" v-for="(tab, index) in tabs">
      <a class="nav-link" :class="{'active': index === currentTab}" role="button" @click="selectTab(index)">{{ tab }}</a>
    </li>
  </ul>
  <div v-for="(tab, index) in tabs" class="">
    <slot :name="`tab${index}`" v-if="currentTab === index"></slot>
  </div>
</template>

<script>
export default {
  name: "Tabs",
  props: {
    tabs: {
      required: true,
      type: Array,
    }
  },
  data() {
    return {
      currentTab: 0,
    }
  },
  methods: {
    selectTab(tab) {
      this.currentTab = tab;
    }
  }
}
</script>

<style scoped>

</style>