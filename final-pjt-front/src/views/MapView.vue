<template>
  <v-container fluid>
    <!-- 검색 입력 및 버튼 -->
    <h1 class="section-title">내 주변 은행 검색하기</h1>
    <br>
    <v-row class="align-center mb-4">
      <v-col cols="12" md="8" class="d-flex">
        <v-text-field
          v-model="searchKeyword"
          label="검색할 장소를 입력하세요"
          @keyup.enter="searchLocation"
          outlined
          dense
          class="flex-grow-1 mr-2"
        />
        <v-btn @click="searchLocation" color="secondary" elevation="2">검색</v-btn>
      </v-col>
    </v-row>

    <!-- 지도와 검색 결과 목록 수평 배치 -->
    <v-row>
      <!-- 지도 영역 -->
      <v-col cols="12" md="6">
        <h1 class="section-title mb-2">지도</h1>
        <div id="map" style="width: 100%; height: 400px;"></div>
      </v-col>

      <!-- 검색 결과 목록 -->
      <v-col cols="12" md="6">
        <!-- 헤더를 리스트 바로 위로 이동 -->
        <h1 class="section-title mb-2">검색 결과</h1>
        <v-list style="height: 400px; overflow-y: auto;">
          <v-list-item
            v-for="(place, index) in places"
            :key="index"
            @click.prevent="moveToLocation(place)"
            style="cursor: pointer;"
          >
            <v-list-item-content>
              <v-list-item-title>{{ place.place_name }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-divider v-if="index < places.length - 1" />
        </v-list>
      </v-col>
    </v-row>

    <!-- 관련 상품 정보 -->
    <h1 class="my-2 section-title" v-if="depositSearch.length || savingSearch.length">관련 상품 정보</h1>

    <!-- 예금 관련 상품 정보 -->
    <h4 class="section-title" v-if="depositSearch.length">예금</h4>
    <v-row v-if="depositSearch.length">
      <v-col v-for="deposit in depositSearch" :key="deposit.id" cols="12" md="6">
        <v-card class="mb-3">
          <v-card-title>{{ deposit.fin_prdt_nm }}</v-card-title>
          <v-card-actions>
            <v-btn @click="movedetail('deposit', deposit.id)" color="primary" text>바로가기</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- 적금 관련 상품 정보 -->
    <h4 class="section-title" v-if="savingSearch.length">적금</h4>
    <v-row v-if="savingSearch.length">
      <v-col v-for="saving in savingSearch" :key="saving.id" cols="12" md="6">
        <v-card class="mb-3">
          <v-card-title>{{ saving.fin_prdt_nm }}</v-card-title>
          <v-card-actions>
            <v-btn @click="movedetail('saving', saving.id)" color="primary" text>바로가기</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- 관련 상품 정보가 없을 때 안내 메시지 -->
    <v-alert v-else type="warning" class="mt-3">
      관련된 상품 정보를 찾아보세요! 검색 후, 나타난 마커를 클릭하면 됩니다!
    </v-alert>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed, onBeforeUnmount } from 'vue';
import { useDepositStore, useSavingStore } from '@/stores/productStores';
import geolocation from 'geolocation';
import Swal from 'sweetalert2';
import router from '@/router';
const movedetail = (type, id) => { router.push({ name: 'ProductDetailView', params: { type, id } }); };
let searchKeyword = ref("");
let map = ref(null);
let ps = ref(null);
let markers = ref([]);
let places = ref([]);
const selected = ref(null);
const depositStore = useDepositStore();
const savingStore = useSavingStore();
const depositSearch = computed(() => depositStore.searchresults);
const savingSearch = computed(() => savingStore.searchresults);

onMounted(() => {
  geolocation.getCurrentPosition((err, position) => {
    if (err) {
      console.error(err);
      initMap(37.5665, 126.9780); // 오류 시 서울 광화문 기본 좌표로 초기화
    } else {
      const { latitude, longitude } = position.coords;
      initMap(latitude, longitude); // 사용자의 현재 위치로 지도 초기화
    }
  });
});

function initMap(latitude, longitude) {
  const container = document.getElementById("map");
  const options = {
    center: new kakao.maps.LatLng(latitude, longitude),
    level: 3,
  };
  map.value = new kakao.maps.Map(container, options);

  // 장소 검색 객체 생성
  ps.value = new kakao.maps.services.Places(map.value);

  // 카테고리로 은행을 검색합니다
  ps.value.categorySearch('BK9', placesSearchCB, { useMapBounds: true });
}

function placesSearchCB(data, status) {
  if (status === kakao.maps.services.Status.OK) {
    places.value = data;
    data.forEach((place) => {
      displayMarker(place);
    });
  }
}

function displayMarker(place) {
  const marker = new kakao.maps.Marker({
    map: map.value,
    position: new kakao.maps.LatLng(place.y, place.x),
  });

  kakao.maps.event.addListener(marker, "click", () => {
    Swal.fire({
      title: `${place.place_name}를 선택하셨습니다.`,
      text: '해당 장소에 대한 상품 정보를 안내드릴까요?',
      icon: 'question',
      showCancelButton: true,
      confirmButtonText: '예',
      cancelButtonText: '아니요'
    }).then((result) => {
      if (result.isConfirmed) {
        selected.value = place.place_name;
        depositStore.searchProducts(selected.value);
        savingStore.searchProducts(selected.value);
      }
    });
  });

  markers.value.push(marker);
}

function searchLocation() {
  if (!searchKeyword.value) {
    alert("검색어를 입력하세요.");
    return;
  }

  // 장소 검색 요청
  ps.value.keywordSearch(searchKeyword.value, (data, status) => {
    if (status === kakao.maps.services.Status.OK) {
      places.value = data;
      displayMarkers(data);
    } else if (status === kakao.maps.services.Status.ZERO_RESULT) {
      alert("검색 결과가 없습니다.");
    } else {
      alert("검색 중 오류가 발생했습니다.");
    }
  });
}

function displayMarkers(placesData) {
  clearMarkers();

  placesData.forEach((place) => {
    const marker = new kakao.maps.Marker({
      map: map.value,
      position: new kakao.maps.LatLng(place.y, place.x),
    });

    kakao.maps.event.addListener(marker, "click", () => {
      Swal.fire({
        title: `${place.place_name}를 선택하셨습니다.`,
        text: '해당 장소에 대한 상품 정보를 안내드릴까요?',
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: '예',
        cancelButtonText: '아니요'
      }).then((result) => {
        if (result.isConfirmed) {
          selected.value = place.place_name;
          depositStore.searchProducts(selected.value);
          savingStore.searchProducts(selected.value);
        }
      });
    });

    markers.value.push(marker);
  });

  const bounds = new kakao.maps.LatLngBounds();
  placesData.forEach((place) => {
    bounds.extend(new kakao.maps.LatLng(place.y, place.x));
  });
  map.value.setBounds(bounds);
}

function clearMarkers() {
  markers.value.forEach((marker) => marker.setMap(null));
  markers.value = [];
}

function moveToLocation(place) {
  const position = new kakao.maps.LatLng(place.y, place.x);
  map.value.setCenter(position);
}

onBeforeUnmount(() => {
  depositStore.searchresults = [];
  savingStore.searchresults = [];
});
</script>

<style scoped>
#map {
  border: 1px solid #ddd;
  border-radius: 4px;
}
</style>
