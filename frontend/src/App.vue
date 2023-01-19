<script>
import { RouterLink, RouterView } from 'vue-router'
import PageHeader from "@/components/page/PageHeader.vue";
import PageFooter from "@/components/page/PageFooter.vue";
import PageTable from "@/components/page/PageTable.vue";

export default {
  components: {PageHeader, PageFooter, PageTable},
  data() {
    return {
      tableData: [
        [`<a href='https://google.com'>google.com</a>`, '22 янв 2023, 23:04:45', `<b class='text-success'>Работает</b>`, `<b class='text-success'>26</b>`, '100'],
        [`<a href='https://google.com'>google.com</a>`, '22 янв 2023, 23:04:45', `<b class='text-success'>Работает</b>`, `<b class='text-success'>26</b>`, '100'],
        [`<a href='https://google.com'>google.com</a>`, '22 янв 2023, 23:04:45', `<b class='text-success'>Работает</b>`, `<b class='text-success'>26</b>`, '100'],
        [`<a href='https://google.com'>google.com</a>`, '22 янв 2023, 23:04:45', `<b class='text-success'>Работает</b>`, `<b class='text-success'>26</b>`, '100'],
        [`<a href='https://google.com'>google.com</a>`, '22 янв 2023, 23:04:45', `<b class='text-success'>Работает</b>`, `<b class='text-success'>26</b>`, '100'],
      ]
    }
  },
  methods: {
    loadMore() {
      this.tableData.push(
          [`<a href='https://google.com'>google.com</a>`, '22 янв 2023, 23:04:45', `<b class='text-success'>Работает</b>`, `<b class='text-success'>26</b>`, '99'],
      );
    }
  }
}
</script>

<template>
<div class="wrapper">
  <PageHeader></PageHeader>
  <div class="container">
    <h1 class="mt-5">Hello, vue + bootstrap</h1>
    <h2 class="text-primary">Some text here</h2>
<!--    <button class="btn btn-primary mt-3">Button</button>-->
    <Btn :class="[ 'mt-3' ]">FGHFGH</Btn>
    <div class="row mt-3">
      <div class="col-7">
        <Block>
          <h3>Hello world</h3>
        </Block>
      </div>
    </div>
    <div class="row">
      <div class="col-12">
        <PageSection :title="`Популярные ресурсы`">
          <Block :class="['mb-2']">
            <Link href="https://google.com">Привет</Link>
          </Block>
          <Block :class="['mb-2']">
            <Link href="https://google.com">Привет</Link>
          </Block>
          <Block :class="['mb-2']">
            <Link href="https://google.com">Привет</Link>
          </Block>
        </PageSection>
      </div>
      <div class="col-12">
        <PageSection :title="`Таблица`">
          <PageTable
              :headers="['Сайт', 'Последняя проверка', 'Состояние', 'Задержка ответа, мс', 'Рейтинг']"
              :data="tableData"
              :noLoadMore="true"

              @loadMore="loadMore"
          ></PageTable>
        </PageSection>
      </div>
    </div>

  </div>
  <PageFooter></PageFooter>
</div>
</template>

<style scoped>
</style>
