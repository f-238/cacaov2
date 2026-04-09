<template>
  <section class="users-stack">
    <div class="summary-grid">
      <article class="summary-card">
        <span class="summary-label">Registered Users</span>
        <strong>{{ filteredUsers.length }}</strong>
      </article>
      <article class="summary-card">
        <span class="summary-label">Active Session</span>
        <strong>{{ currentUserName }}</strong>
      </article>
    </div>

    <div class="panel">
      <div class="panel-head">
        <div>
          <h3>User Management</h3>
          <p>Search, filter, edit, and remove local admin user records.</p>
        </div>
      </div>

      <div class="toolbar">
        <label class="search-field">
          <span class="search-icon" aria-hidden="true">
            <svg viewBox="0 0 24 24" focusable="false">
              <path d="M10 2a8 8 0 1 0 5.29 14l4.35 4.35 1.41-1.41-4.35-4.35A8 8 0 0 0 10 2Zm0 2a6 6 0 1 1-6 6 6 6 0 0 1 6-6Z" />
            </svg>
          </span>
          <input
            v-model.trim="searchQuery"
            type="search"
            placeholder="Search name, email, or phone"
          >
        </label>

        <label class="filter-field">
          <span>Role</span>
          <select v-model="roleFilter">
            <option value="All">All Roles</option>
            <option value="Admin">Admin</option>
            <option value="Manager">Manager</option>
            <option value="Viewer">Viewer</option>
          </select>
        </label>

        <label class="filter-field">
          <span>Status</span>
          <select v-model="statusFilter">
            <option value="All">All Statuses</option>
            <option value="Active">Active</option>
            <option value="Inactive">Inactive</option>
            <option value="Pending">Pending</option>
          </select>
        </label>
      </div>

      <div v-if="filteredUsers.length > 0" class="desktop-table">
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Phone</th>
              <th>Role</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in filteredUsers" :key="user.email">
              <template v-if="editingEmail === user.email">
                <td><input v-model.trim="draftUser.fullName" class="inline-input"></td>
                <td><input v-model.trim="draftUser.email" class="inline-input" type="email"></td>
                <td><input v-model.trim="draftUser.phone" class="inline-input"></td>
                <td>
                  <select v-model="draftUser.role" class="inline-input inline-select">
                    <option>Admin</option>
                    <option>Manager</option>
                    <option>Viewer</option>
                  </select>
                </td>
                <td>
                  <select v-model="draftUser.status" class="inline-input inline-select">
                    <option>Active</option>
                    <option>Inactive</option>
                    <option>Pending</option>
                  </select>
                </td>
                <td>
                  <div class="action-row">
                    <button class="action-button save" @click="saveEdit(user.email)">
                      Save
                    </button>
                    <button class="action-button ghost" @click="cancelEdit">
                      Cancel
                    </button>
                  </div>
                </td>
              </template>

              <template v-else>
                <td>{{ user.fullName }}</td>
                <td>{{ user.email }}</td>
                <td>{{ user.phone || 'N/A' }}</td>
                <td>
                  <span class="pill role-pill">{{ user.role }}</span>
                </td>
                <td>
                  <span class="pill" :class="statusClass(user.status)">{{ user.status }}</span>
                </td>
                <td>
                  <div class="action-row">
                    <button class="icon-button edit" @click="startEdit(user)" aria-label="Edit user">
                      <svg viewBox="0 0 24 24" focusable="false">
                        <path d="m3 17.25 9.81-9.81 3.75 3.75L6.75 21H3Zm14.71-9.04a1 1 0 0 0 0-1.42l-2.5-2.5a1 1 0 0 0-1.42 0l-1.56 1.56 3.75 3.75Z" />
                      </svg>
                    </button>
                    <button class="icon-button delete" @click="removeUser(user.email)" aria-label="Delete user">
                      <svg viewBox="0 0 24 24" focusable="false">
                        <path d="M9 3h6l1 2h5v2H3V5h5Zm1 7h2v8h-2Zm4 0h2v8h-2ZM7 10h2v8H7Zm1 11a2 2 0 0 1-2-2V8h12v11a2 2 0 0 1-2 2Z" />
                      </svg>
                    </button>
                  </div>
                </td>
              </template>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="mobile-cards" v-if="filteredUsers.length > 0">
        <article v-for="user in filteredUsers" :key="`mobile-${user.email}`" class="user-card">
          <template v-if="editingEmail === user.email">
            <input v-model.trim="draftUser.fullName" class="inline-input" placeholder="Name">
            <input v-model.trim="draftUser.email" class="inline-input" type="email" placeholder="Email">
            <input v-model.trim="draftUser.phone" class="inline-input" placeholder="Phone">
            <select v-model="draftUser.role" class="inline-input inline-select">
              <option>Admin</option>
              <option>Manager</option>
              <option>Viewer</option>
            </select>
            <select v-model="draftUser.status" class="inline-input inline-select">
              <option>Active</option>
              <option>Inactive</option>
              <option>Pending</option>
            </select>
            <div class="action-row">
              <button class="action-button save" @click="saveEdit(user.email)">Save</button>
              <button class="action-button ghost" @click="cancelEdit">Cancel</button>
            </div>
          </template>

          <template v-else>
            <div class="user-card-top">
              <div>
                <h4>{{ user.fullName }}</h4>
                <p>{{ user.email }}</p>
              </div>
              <span class="pill" :class="statusClass(user.status)">{{ user.status }}</span>
            </div>

            <div class="card-meta">
              <span><strong>Phone:</strong> {{ user.phone || 'N/A' }}</span>
              <span><strong>Role:</strong> {{ user.role }}</span>
            </div>

            <div class="action-row">
              <button class="action-button edit" @click="startEdit(user)">Edit</button>
              <button class="action-button delete" @click="removeUser(user.email)">Delete</button>
            </div>
          </template>
        </article>
      </div>

      <p v-if="filteredUsers.length === 0" class="empty-copy">No users match the current search and filters.</p>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, reactive, ref } from 'vue'

type UserRole = 'Admin' | 'Manager' | 'Viewer'
type UserStatus = 'Active' | 'Inactive' | 'Pending'

type StoredUser = {
  fullName: string
  email: string
  phone?: string
  role?: UserRole
  status?: UserStatus
  createdAt?: string
  password?: string
}

const props = defineProps<{
  currentUserName: string
}>()

const searchQuery = ref('')
const roleFilter = ref<'All' | UserRole>('All')
const statusFilter = ref<'All' | UserStatus>('All')
const editingEmail = ref('')
const users = ref<StoredUser[]>(loadUsers())

const draftUser = reactive<StoredUser>({
  fullName: '',
  email: '',
  phone: '',
  role: 'Viewer',
  status: 'Active'
})

function normalizeUser(user: StoredUser, index: number): StoredUser {
  const defaultRole: UserRole[] = ['Admin', 'Manager', 'Viewer']
  const defaultStatus: UserStatus[] = ['Active', 'Pending', 'Inactive']

  return {
    ...user,
    phone: user.phone ?? '',
    role: user.role ?? defaultRole[index % defaultRole.length],
    status: user.status ?? defaultStatus[index % defaultStatus.length]
  }
}

function loadUsers() {
  const storedUsers = localStorage.getItem('users')

  if (!storedUsers) {
    return []
  }

  try {
    const parsed = JSON.parse(storedUsers) as StoredUser[]
    return Array.isArray(parsed) ? parsed.map(normalizeUser) : []
  } catch {
    return []
  }
}

function persistUsers() {
  localStorage.setItem('users', JSON.stringify(users.value))
}

const filteredUsers = computed(() => {
  const query = searchQuery.value.toLowerCase()

  return users.value.filter((user) => {
    const matchesQuery =
      !query ||
      user.fullName.toLowerCase().includes(query) ||
      user.email.toLowerCase().includes(query) ||
      (user.phone ?? '').toLowerCase().includes(query)

    const matchesRole = roleFilter.value === 'All' || user.role === roleFilter.value
    const matchesStatus = statusFilter.value === 'All' || user.status === statusFilter.value

    return matchesQuery && matchesRole && matchesStatus
  })
})

function startEdit(user: StoredUser) {
  editingEmail.value = user.email
  Object.assign(draftUser, user)
}

function cancelEdit() {
  editingEmail.value = ''
}

function saveEdit(originalEmail: string) {
  const nextEmail = draftUser.email?.trim() ?? ''
  const nextName = draftUser.fullName?.trim() ?? ''

  if (!nextName || !nextEmail) {
    return
  }

  users.value = users.value.map((user) =>
    user.email === originalEmail
      ? normalizeUser(
          {
            ...user,
            fullName: nextName,
            email: nextEmail,
            phone: draftUser.phone?.trim() ?? '',
            role: draftUser.role,
            status: draftUser.status
          },
          0
        )
      : user
  )

  persistUsers()
  cancelEdit()
}

function removeUser(email: string) {
  users.value = users.value.filter((user) => user.email !== email)
  persistUsers()

  if (editingEmail.value === email) {
    cancelEdit()
  }
}

function statusClass(status?: UserStatus) {
  return {
    active: status === 'Active',
    pending: status === 'Pending',
    inactive: status === 'Inactive'
  }
}
</script>

<style scoped>
.users-stack {
  display: grid;
  gap: 20px;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.summary-card,
.panel {
  padding: 22px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid #efe3e7;
  box-shadow: 0 22px 50px rgba(36, 48, 66, 0.08);
}

.summary-label {
  color: #6b788c;
  font-size: 0.92rem;
  font-weight: 600;
}

.summary-card strong {
  display: block;
  margin-top: 10px;
  font-size: 1.35rem;
  color: #243042;
}

.panel-head {
  margin-bottom: 16px;
}

.panel-head h3 {
  margin: 0;
  color: #243042;
}

.panel-head p,
.empty-copy {
  margin: 10px 0 0;
  color: #5f6d81;
  line-height: 1.6;
}

.toolbar {
  display: grid;
  grid-template-columns: minmax(240px, 1.2fr) repeat(2, minmax(160px, 0.5fr));
  gap: 12px;
  margin-bottom: 18px;
}

.search-field,
.filter-field {
  display: grid;
  gap: 6px;
}

.search-field span,
.filter-field span {
  color: #526075;
  font-size: 0.92rem;
  font-weight: 600;
}

.search-field {
  position: relative;
}

.search-icon {
  position: absolute;
  left: 14px;
  bottom: 12px;
  width: 18px;
  height: 18px;
  color: #7a8799;
}

.search-icon svg,
.icon-button svg {
  width: 100%;
  height: 100%;
  fill: currentColor;
  display: block;
}

.search-field input,
.filter-field select,
.inline-input {
  min-height: 44px;
  padding: 0 12px;
  border: 1px solid #e6dce2;
  border-radius: 14px;
  background: #fff;
  color: #243042;
}

.search-field input {
  padding-left: 42px;
}

.search-field input:focus,
.filter-field select:focus,
.inline-input:focus {
  outline: none;
  border-color: #d9a6b8;
  box-shadow: 0 0 0 4px rgba(233, 189, 204, 0.25);
}

.desktop-table {
  display: block;
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 14px 12px;
  text-align: left;
  border-bottom: 1px solid #f1e8ec;
}

th {
  color: #526075;
  font-size: 0.92rem;
}

tbody tr:last-child td {
  border-bottom: 0;
}

.pill {
  display: inline-flex;
  align-items: center;
  padding: 7px 12px;
  border-radius: 999px;
  font-size: 0.88rem;
  font-weight: 700;
}

.role-pill {
  background: #eef6ff;
  color: #4d7bb5;
}

.active {
  background: #effaf5;
  color: #3b9274;
}

.pending {
  background: #fff7e8;
  color: #b88a2b;
}

.inactive {
  background: #fff1f3;
  color: #c05c72;
}

.action-row {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.icon-button,
.action-button {
  min-height: 38px;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
}

.icon-button {
  width: 38px;
  padding: 8px;
  border: 0;
}

.icon-button.edit,
.action-button.edit {
  background: #eef6ff;
  color: #4d7bb5;
}

.icon-button.delete,
.action-button.delete {
  background: #fff1f3;
  color: #c05c72;
}

.action-button.save {
  padding: 0 12px;
  border: 0;
  background: linear-gradient(135deg, #f3a6ba, #9fd9cc);
  color: #1f2937;
}

.action-button.ghost {
  padding: 0 12px;
  border: 1px solid #eadfe5;
  background: rgba(255, 255, 255, 0.88);
  color: #526075;
}

.mobile-cards {
  display: none;
}

.user-card {
  display: grid;
  gap: 14px;
  padding: 18px;
  border-radius: 18px;
  background: #fffdfd;
  border: 1px solid #f3eaee;
}

.user-card-top {
  display: flex;
  justify-content: space-between;
  gap: 12px;
}

.user-card-top h4 {
  margin: 0;
  color: #243042;
}

.user-card-top p,
.card-meta {
  margin: 6px 0 0;
  color: #607085;
}

.card-meta {
  display: grid;
  gap: 6px;
}

.inline-select {
  width: 100%;
}

@media (max-width: 900px) {
  .toolbar {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 720px) {
  .summary-grid {
    grid-template-columns: 1fr;
  }

  .desktop-table {
    display: none;
  }

  .mobile-cards {
    display: grid;
    gap: 12px;
  }

  .summary-card,
  .panel {
    border-radius: 22px;
  }
}
</style>
