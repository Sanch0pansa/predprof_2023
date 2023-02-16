<template>
  <div class="col-12">
    <nav aria-label="breadcrumb">
      <ol class="breadcrumb">
        <li :class="`breadcrumb-item ${link.cur ? 'active' : ''}`" v-for="link in links"><RouterLink :to="{name: link.route_name}">{{ link.name }}</RouterLink></li>
      </ol>
    </nav>
  </div>

</template>

<script>
export default {
  name: "PageBreadcrumbs",
  props: {
    linksNames: {
      type: Array,
      required: true,
    }
  },
  data() {

    let linksKeys = {
      'single': {name: 'Ресурс', route_name: 'single_page'},
      'checker': {name: 'Отчёт', route_name: 'checker'},
      'account': {name: 'Личный кабинет', route_name: 'account'},
      'telegram': {name: 'Привязка Telegram', route_name: 'verify_telegram'},
      'edit_account': {name: 'Редактирование', route_name: 'edit_account'},
      'moderation': {name: 'Модер. панель', route_name: 'moderation'},
      'moderation_pages': {name: 'Ресурсы', route_name: 'moderation_pages'},
      'moderation_reports': {name: 'Сообщения о сбоях', route_name: 'moderation_reports'},
      'moderation_reviews': {name: 'Отзывы', route_name: 'moderation_reviews'},
      'admin': {name: 'Админ. панель', route_name: 'admin'},
      'create_page': {name: 'Добавление ресурса', route_name: 'create_page'},
    };

    let links = this.linksNames.map(name => linksKeys[name]);
    links[links.length - 1].cur = true;

    return {
      links: [
          {name: 'Главная', route_name: 'home'},
          ...links
      ]
    }
  }
}
</script>

<style scoped>

</style>