//<svg>'s for icons
const iconSaveTask = `<svg class="svg-icon" viewBox="0 0 20 20">
                         <path fill="none" d="M9.917,0.875c-5.086,0-9.208,4.123-9.208,9.208c0,5.086,4.123,9.208,9.208,9.208s9.208-4.122,9.208-9.208
                             C19.125,4.998,15.003,0.875,9.917,0.875z M9.917,18.141c-4.451,0-8.058-3.607-8.058-8.058s3.607-8.057,8.058-8.057
                             c4.449,0,8.057,3.607,8.057,8.057S14.366,18.141,9.917,18.141z M13.851,6.794l-5.373,5.372L5.984,9.672
                             c-0.219-0.219-0.575-0.219-0.795,0c-0.219,0.22-0.219,0.575,0,0.794l2.823,2.823c0.02,0.028,0.031,0.059,0.055,0.083
                             c0.113,0.113,0.263,0.166,0.411,0.162c0.148,0.004,0.298-0.049,0.411-0.162c0.024-0.024,0.036-0.055,0.055-0.083l5.701-5.7
                             c0.219-0.219,0.219-0.575,0-0.794C14.425,6.575,14.069,6.575,13.851,6.794z"></path>
                      </svg>`

const iconCloseEditor = `<svg class="svg-icon" viewBox="0 0 20 20">
                            <path fill="none" d="M13.864,6.136c-0.22-0.219-0.576-0.219-0.795,0L10,9.206l-3.07-3.07c-0.219-0.219-0.575-0.219-0.795,0
                                c-0.219,0.22-0.219,0.576,0,0.795L9.205,10l-3.07,3.07c-0.219,0.219-0.219,0.574,0,0.794c0.22,0.22,0.576,0.22,0.795,0L10,10.795
                                l3.069,3.069c0.219,0.22,0.575,0.22,0.795,0c0.219-0.22,0.219-0.575,0-0.794L10.794,10l3.07-3.07
                                C14.083,6.711,14.083,6.355,13.864,6.136z M10,0.792c-5.086,0-9.208,4.123-9.208,9.208c0,5.085,4.123,9.208,9.208,9.208
                                s9.208-4.122,9.208-9.208C19.208,4.915,15.086,0.792,10,0.792z M10,18.058c-4.451,0-8.057-3.607-8.057-8.057
                                c0-4.451,3.606-8.057,8.057-8.057c4.449,0,8.058,3.606,8.058,8.057C18.058,14.45,14.449,18.058,10,18.058z"></path>
                         </svg>`

const iconEditTask = `<svg class="svg-icon" viewBox="0 0 20 20">
                          <path d="M10,2.172c-4.324,0-7.828,3.504-7.828,7.828S5.676,17.828,10,17.828c4.324,0,7.828-3.504,7.828-7.828S14.324,2.172,10,2.172M10,17.004c-3.863,0-7.004-3.141-7.004-7.003S6.137,2.997,10,2.997c3.862,0,7.004,3.141,7.004,7.004S13.862,17.004,10,17.004M10,8.559c-0.795,0-1.442,0.646-1.442,1.442S9.205,11.443,10,11.443s1.441-0.647,1.441-1.443S10.795,8.559,10,8.559 M10,10.619c-0.34,0-0.618-0.278-0.618-0.618S9.66,9.382,10,9.382S10.618,9.661,10.618,10S10.34,10.619,10,10.619 M14.12,8.559c-0.795,0-1.442,0.646-1.442,1.442s0.647,1.443,1.442,1.443s1.442-0.647,1.442-1.443S14.915,8.559,14.12,8.559 M14.12,10.619c-0.34,0-0.618-0.278-0.618-0.618s0.278-0.618,0.618-0.618S14.738,9.661,14.738,10S14.46,10.619,14.12,10.619 M5.88,8.559c-0.795,0-1.442,0.646-1.442,1.442s0.646,1.443,1.442,1.443S7.322,10.796,7.322,10S6.675,8.559,5.88,8.559 M5.88,10.619c-0.34,0-0.618-0.278-0.618-0.618S5.54,9.382,5.88,9.382S6.498,9.661,6.498,10S6.22,10.619,5.88,10.619"></path>
                      </svg>`

const iconDeleteTask = `<svg class="svg-icon" viewBox="0 0 20 20">
                            <path d="M17.114,3.923h-4.589V2.427c0-0.252-0.207-0.459-0.46-0.459H7.935c-0.252,0-0.459,0.207-0.459,0.459v1.496h-4.59c-0.252,0-0.459,0.205-0.459,0.459c0,0.252,0.207,0.459,0.459,0.459h1.51v12.732c0,0.252,0.207,0.459,0.459,0.459h10.29c0.254,0,0.459-0.207,0.459-0.459V4.841h1.511c0.252,0,0.459-0.207,0.459-0.459C17.573,4.127,17.366,3.923,17.114,3.923M8.394,2.886h3.214v0.918H8.394V2.886z M14.686,17.114H5.314V4.841h9.372V17.114z M12.525,7.306v7.344c0,0.252-0.207,0.459-0.46,0.459s-0.458-0.207-0.458-0.459V7.306c0-0.254,0.205-0.459,0.458-0.459S12.525,7.051,12.525,7.306M8.394,7.306v7.344c0,0.252-0.207,0.459-0.459,0.459s-0.459-0.207-0.459-0.459V7.306c0-0.254,0.207-0.459,0.459-0.459S8.394,7.051,8.394,7.306"></path>
                        </svg>`

const iconAddTask = `<svg class="svg-icon" viewBox="0 0 20 20">
                        <path fill="none" d="M13.388,9.624h-3.011v-3.01c0-0.208-0.168-0.377-0.376-0.377S9.624,6.405,9.624,6.613v3.01H6.613c-0.208,0-0.376,0.168-0.376,0.376s0.168,0.376,0.376,0.376h3.011v3.01c0,0.208,0.168,0.378,0.376,0.378s0.376-0.17,0.376-0.378v-3.01h3.011c0.207,0,0.377-0.168,0.377-0.376S13.595,9.624,13.388,9.624z M10,1.344c-4.781,0-8.656,3.875-8.656,8.656c0,4.781,3.875,8.656,8.656,8.656c4.781,0,8.656-3.875,8.656-8.656C18.656,5.219,14.781,1.344,10,1.344z M10,17.903c-4.365,0-7.904-3.538-7.904-7.903S5.635,2.096,10,2.096S17.903,5.635,17.903,10S14.365,17.903,10,17.903z"></path>
                     </svg>`

const iconPointLeft = `<svg class="svg-icon" viewBox="0 0 20 20">
                           <path fill="none" d="M8.388,10.049l4.76-4.873c0.303-0.31,0.297-0.804-0.012-1.105c-0.309-0.304-0.803-0.293-1.105,0.012L6.726,9.516c-0.303,0.31-0.296,0.805,0.012,1.105l5.433,5.307c0.152,0.148,0.35,0.223,0.547,0.223c0.203,0,0.406-0.08,0.559-0.236c0.303-0.309,0.295-0.803-0.012-1.104L8.388,10.049z"></path>
                       </svg>`

const iconPoinRight = `<svg class="svg-icon" viewBox="0 0 20 20">
                          <path fill="none" d="M11.611,10.049l-4.76-4.873c-0.303-0.31-0.297-0.804,0.012-1.105c0.309-0.304,0.803-0.293,1.105,0.012l5.306,5.433c0.304,0.31,0.296,0.805-0.012,1.105L7.83,15.928c-0.152,0.148-0.35,0.223-0.547,0.223c-0.203,0-0.406-0.08-0.559-0.236c-0.303-0.309-0.295-0.803,0.012-1.104L11.611,10.049z"></path>
                       </svg>`



class DateFormater {

    static _monthsRU = {
        0: 'Январь',
        1: 'Февраль',
        2: 'Март',
        3: 'Апрель',
        4: 'Май',
        5: 'Июнь',
        6: 'Июль',
        7: 'Август',
        8: 'Сентябрь',
        9: 'Октябрь',
        10: 'Ноябрь',
        11: 'Декабрь',
    }

    static _daysOfWeekRU = {
        1: 'Понедельник',
        2: 'Вторник',
        3: 'Среда',
        4: 'Четверг',
        5: 'Пятница',
        6: 'Суббота',
        0: 'Воскесенье',
    }

    static makeMonthLabel(dateObj) {
        let month = this._monthsRU[dateObj.getMonth()]
        let year = dateObj.getYear() + 1900
        return `${month}, ${year}`
    }

    static makeTaskListLabel(dateObj) {
        let dateTimeString = this.formatForBackend(dateObj)
        return dateTimeString.slice(0, 10)
    }

    // static formatForBackend(dateObj) {
    //     // Swedish locale returns the most suitable for further processing
    //     // date-string format: YYYY-MM-DD HH:MM:SS
    //     return dateObj.toLocaleString('sv-SE')
    // }

    static formatForBackend(dateObj) {
        let jsISOStirng = dateObj.toISOString()
        let properISOString = jsISOStirng.slice(0, -1)
        return properISOString + '+00:00'
    }

}


class TransportService {
    
    getChangeMonthPack(date) {
        // let formattedDate = DateFormater.formatForBackend(date)
        // return eel.send_to_client('changeMonthPack', formattedDate)()
        
        return fetch('http://127.0.0.1:8000/taskmanager/test')
            .then(response => response.json())
    }

    // addNewTask(taskObj) {
    //     return eel.send_to_client('addNewTask', taskObj)()
    // }

    // changeTask(taskObj) {
    //     return eel.send_to_client('changeTask', taskObj)()
    // }

    // deleteTask(taskObj) {
    //     return eel.send_to_client('deleteTask', taskObj)()
    // }

    // checkUncheckTask(taskObj) {
    //     return eel.send_to_client('checkUncheckTask', taskObj)()
    // }

} 


class TaskObject {
    constructor(object) {
    this.ID = object.ID
    this.date = object.date
    this.initdate = object.initdate
    this.title = object.title
    this.description = object.description
    this.completion = object.completion
    this._interval
    this.interval = object.interval
    this._autoshift
    this.autoshift = object.autoshift
    this._files
    this.files = object.files
    }

    set interval(newValue) {
        if (this.autoshift === 'no' || !this.autoshift) {
            this._interval = newValue
        } else {
            throw `cannot assign interval to the task 
                   where exist autoshift value`
        } 
    }

    get interval() {
        return this._interval
    }

    set autoshift(newValue) {
        if (this.interval === 'no' || !this.interval) {
            this._autoshift = newValue
        } else {
            throw `cannot assign autoshift to the task 
                   where exist interval value`
        }
    }

    get autoshift() {
        return this._autoshift
    }

    static getEmpty(definedValues) {
        let taskObj = new TaskObject({
            ID: undefined,
            date: undefined,
            initdate: undefined,
            title: '',
            description: '',
            completion: false,
            interval: 'no',
            autoshift: 'no',
            files: [],
        })
        if(definedValues) {
            Object.assign(taskObj, definedValues)
        }
        return taskObj
    }
}


class CacheServis {
    constructor(transportService) {
        this.transportService = transportService
        this.currentDate = new Date()
        
        this.pageDate = this.currentDate
        this.pageDaysArr = 'not received yet'
        this.taskList = 'not received yet'
        // the promise, that indicates receiving of data from the server
        this.readyToRun = this._requestDataPack(this.currentDate)  
    }

    _requestDataPack(date) {
        // returns promise, that indicates receiving data from server
        return transportService.getChangeMonthPack(date)
            .then(pack => {
                this.pageDate = date
                this.pageDaysArr = pack.monthdates.map(i => new Date(i))
                this.taskList = pack.tasks
                console.log('%c requested data successfully received from the server', 
                    'color: yellowgreen')
                console.log(this.taskList)
            })
    }

    reqChangeDate(newDate) {
        // also returns promise, that indicates receiving data from server
        console.log(`%c requesting data for changing page date: 
                    ${DateFormater.formatForBackend(this.pageDate)}`,
                    'color: cornflowerblue')
        return this._requestDataPack(newDate)
            .catch(err => {
                console.log(`%c Failed to recieve data for changing page date: 
                ${DateFormater.formatForBackend(this.pageDate)}`,
                'color: crimson')
                throw err
            })
    }

    refreshData() {
        return this.reqChangeDate(this.pageDate)
    }

    isDateInMonth(date) {
        return date.getMonth() === this.pageDate.getMonth()
    }

    checkDailyTasks(date) {
        let dateString = DateFormater.formatForBackend(date)
        let haveDoneTasks = false
        
        console.log(dateString)
        for (let task of this.taskList) {
            if (task.date === dateString) {
                if (!task.completion) {
                    return 'got tasks'
                } else {
                    haveDoneTasks = true
                }
            }
        }
        if (haveDoneTasks) {
            return 'tasks done'
        } else {
            return 'no tasks'
        }
    }

    getDailyTasks(date){
        let dateString = DateFormater.formatForBackend(date)
        let dailyTasks = []

        for(let task of this.taskList) {
            if (dateString === task.date){
                dailyTasks.push(task)
            }
        }
        return dailyTasks
    }

    createTask(newTask) {
        return this.transportService.addNewTask(newTask)
            .then(() => {
                console.log('%c the task successfully added to DB', 'color: yellowgreen')
            })
            .then(() => this.refreshData())
            .catch(err => {
                console.error('fail to add the task')
                throw err
            })
    }

    editTask(changedFields) {
        return this.transportService.changeTask(changedFields)
            .then(() => {
                console.log('%c the task successfully changed at DB', 'color: yellowgreen')
            })
            .then(() => this.refreshData())
            .catch(err => {
                console.error('fail to edit the task')
                throw err
            })
    }

    deleteTask(deletedTask) {
        return this.transportService.deleteTask(deletedTask)
            .then(() => {
                console.log('%c the task was successfully deleted from DB', 'color: yellowgreen')
                let taskIndex = this.taskList.indexOf(deletedTask)
                this.taskList.splice(taskIndex, 1)
            })
            .catch(err => {
                console.error('failed to delete the task')
                throw err
            })
    }

    checkUncheckTask(checkingTask) {
        return this.transportService.checkUncheckTask(checkingTask)
            .then(() => {
                console.log('%c information about the task completion was changed on DB', 'color: yellowgreen')
                let unchangedTask
                for(let task of this.taskList) {
                    if(task.ID === checkingTask.ID && task.date === checkingTask.date) {
                        task.completion = checkingTask.completion
                        break
                    }
                }
            })
            .catch(err => {
                console.error('failed to change information about the task completion on DB')
                throw err
            })
    }
}





class Wiget {
    constructor(parent, options={}, tag='div') {
        this.parent = parent
        this.tag = tag
        this.element = document.createElement(this.tag)
        this.id = options.id ? options.id : this.makeId('w')
        this.options = options
        // E.i. flex, box etc. For used in hide() and show() methods.
        this._defaultDisplayMode
        // Keeps available the options, that was given on instance constructor - otherwise,
        // they would be assign via setter to the this.element object and not available any more.
        this._localOptions = options
    }
 
    // The alternative constructor, that takes as args parent wiget and raw
    // html string and returns a new wiget object based on given http string 
    static fromHTML(parent, rawHTML) {
        let element = Wiget.makeElementFromHTML(rawHTML)
        let wiget = new Wiget(parent)
        wiget.element = element
        wiget.tag = element.tagName

        return wiget
    }

    // creates html element from a raw html string
    static makeElementFromHTML(rawHTML) {
        let parser = new DOMParser()
        let newDoc = parser.parseFromString(rawHTML, 'text/html')
        let element = newDoc.body.firstElementChild
        
        return element
    }

    build() {
        try {
            this.element.id = this.id
            let parentNode = document.getElementById(this.parent.id)
            parentNode.insertAdjacentElement('beforeend', this.element)
            this._defaultDisplayMode = this.element.style.display
        } catch (err) {
            console.error('cannot build wiget:', this)
            throw(err)
        }
    }

    isBuilded(){
        if(document.getElementById(this.id)){
            return true
        } else {
            return false
        }
    }

    set options(newOptions) {
        Object.assign(this.element, newOptions)
    }

    makeId(typeChar) {
        let randInt = Math.floor(Math.random() * 99999)
        return typeChar + randInt
    }

    remove() {
        this.element.remove()
    }

    hide() {
        if(this._defaultDisplayMode != 'none'){
            let currentMode = this.element.style.display
            this.element._defaultDisplayMode = currentMode
        }
        this.element.style.display = 'none'
    }

    show() {
        this.element.style.display = this._defaultDisplayMode
    }

    disable() {
        this.element.disabled = true
    }

    enable() {
        this.element.disabled = false
    }

    addCssClass(className) {
        this.element.classList.add(className)
    }

    removeCssClass(className) {
        this.element.classList.remove(className)
    }
}


class iconButton24 extends Wiget {
    constructor(parent, options={}, svgHTML) {
        super(parent, options)
        this.tag = 'button'
        this.element = document.createElement(this.tag)
        this.element.className = 'button-icon24'

        this.SvgIcon = Wiget.fromHTML(this, svgHTML)
    }

    build(){
        super.build()
        this.SvgIcon.build()
        if(this._localOptions.onclick) {
            this.element.onclick = this._localOptions.onclick
        }
        if (this._localOptions.context) {
            this.element.context = this._localOptions.context
        }
    }
}


class Calendar extends Wiget {
    constructor (parent, cacheServis) {
        super(parent)
        
        this.id = 'c-calendar'
        this.cacheServis = cacheServis
        
        this.date = this.cacheServis.currentDate
        this.daysArr = this.cacheServis.pageDaysArr

        // Child wigets
        this.childWigets = [
            this.Topbar = new Wiget(this, {id: 'c-topbar'}),

            this.DaysFrame = new Wiget(this, {id: 'c-daysFrame'}),
            
            this.PrevMonthBtn = new iconButton24(this.Topbar, {
                id: 'monthBack-bt', 
                onclick: this.toPrevMonth.bind(this),
            }, iconPointLeft),
            
            this.MonthLabel = new Wiget(this.Topbar, {
                id: 'c-topbar__monthLabel',
                innerText: DateFormater.makeMonthLabel(this.date)
            }),
            
            this.NextMonthBtn = new iconButton24(this.Topbar, {
                id: 'monthForv-bt', 
                onclick: this.toNextMonth.bind(this),
            }, iconPoinRight)
        ]

        this.DayButtonArr = this.initDayButtons(this.DaysFrame, this.daysArr)

        // some cosmetic appearence fixes
        this.PrevMonthBtn.addCssClass('c-topbar__swtcMonthBt')
        this.NextMonthBtn.addCssClass('c-topbar__swtcMonthBt')
    }

    build() {
        super.build()
        
        this.childWigets.forEach(ch => ch.build())
        this.DayButtonArr.forEach(btn => btn.build())
    }


    initDayButtons(frame, daysArr) {
        let array = []
        for(let date of daysArr) {
            let btn = new DayButton(frame, date, this.cacheServis)
            array.push(btn)
        }
        return array
    }
    
    configurateDayButtons(newDateList) {
        let index = 0
        for (let btn of this.DayButtonArr) {
            btn.configurate(newDateList[index])
            index += 1
        }   
    }

    updDayButtonsStatus(){
        this.DayButtonArr.forEach(bt => bt.updStatus())
    }

    reqChangeDate(newDate) {
        this.cacheServis.reqChangeDate(newDate)
            .then(data => {
                return new Promise( (rs, rj) => {
                    this.date = this.cacheServis.pageDate
                    this.daysArr = this.cacheServis.pageDaysArr
                    this.configurateDayButtons(this.cacheServis.pageDaysArr)
                    this.MonthLabel.element.innerText = DateFormater.makeMonthLabel(this.date)
                })
            })
            .catch(err => {
                // TODO: proper error handling 
                console.log('error catched in the end-point')
                throw err
            })
    }

    toNextMonth() {
        let newMonth, newYear
        if (this.date.getMonth() === 11) {
            newMonth = 0
            newYear = this.date.getYear() + 1 + 1900
        } else {
            newMonth = this.date.getMonth() + 1
            newYear = this.date.getYear() + 1900
        }
        
        let newDate = new Date(newYear, newMonth) 
        this.reqChangeDate(newDate)
    }

    toPrevMonth() {
        let newMonth, newYear
        if (this.date.getMonth() === 0) {
            newMonth = 11
            newYear = this.date.getYear() - 1 + 1900
        } else {
            newMonth = this.date.getMonth() - 1
            newYear = this.date.getYear() + 1900
        }

        let newDate = new Date(newYear, newMonth) 
        this.reqChangeDate(newDate)
    }

    refreshMonth() {
        this.reqChangeDate(this.date)
    }

}


class DayButton extends Wiget {
    constructor(parent, date, cacheServis) {
        super(parent)
        this.tag = 'button'
        this.element = document.createElement(this.tag)
        this.id = this.makeId('dBtn')
        this.element.className = 'c-daysFrame__dayButton'
        
        this.cacheServis = cacheServis
        this.date = date

        this.options = {
            onclick: this.boundSelf.bind(this),
        }

        this.configurate(this.date)
    }

    updStatus() {
        let status = this.cacheServis.checkDailyTasks(this.date)
        let classList = this.element.classList  // shortcut

        if (status === 'no tasks') {
            classList.add('--no-tasks')
            classList.remove('--tasks-done', '--got-tasks')
        } else if (status === 'tasks done') {
            classList.add('--tasks-done')
            classList.remove('--no-tasks', '--got-tasks')
        } else if (status === 'got tasks') {
            classList.add('--got-tasks')
            classList.remove('--no-tasks', '--tasks-done') 
        } else {
            throw Error('no such status: ' + status)
        }
    }

    configurate(newDate) {
        this.date = newDate
        this.element.innerText = newDate.getDate()
        
        this.updStatus()

        if (!this.cacheServis.isDateInMonth(newDate)) {
            this.element.classList.add('--out-month')
        } else {
            this.element.classList.remove('--out-month')
        } 
    }

    reqChangeDate(newDate) {
        this.date = newDate
        this.configurate(newDate)
    }

    boundSelf(){
        taskPanel.boundDayBt(this)
    }

}


class TaskPanel extends Wiget {
    constructor(parent, cacheServis) {
        super(parent)
        
        this.id = 'tp-taskpanel'
        this.cacheServis = cacheServis

        // the appropriate DayButton on the callendar widget, which have the same date.
        this.relatedDayButton 

        // Child wigets
        this.Topbar = new Wiget(this, {
            id: 'tp-topbar',
        })
        this.DateLabel = new Wiget(this.Topbar, {
            id: 'tp-dateLabel',
            innerText: 'Date label'
        })
        this.TaskList = new TaskList(this)
        
        this.CreateTaskBt = new iconButton24(this.Topbar, {
            id: 'tp-createTaskBt',
            onclick: this.TaskList.openTaskAdder.bind(this.TaskList)
            }, iconAddTask)
    }
    
    get dailyTaskArray(){
        if (this.relatedDayButton) {
            let date = this.relatedDayButton.date
            return this.cacheServis.getDailyTasks(date)
        } else {
            return []
        }
    }

    build() {
        super.build()

        this.Topbar.build()
        this.DateLabel.build()
        this.TaskList.build()
    }

    boundDayBt(dayButton) {
        
        this.relatedDayButton = dayButton
        this.TaskList.update()
        this.DateLabel.element.innerText = DateFormater.makeTaskListLabel(dayButton.date)
        if(!this.CreateTaskBt.isBuilded()) {
            this.CreateTaskBt.build()
        }
    }

}       


class TaskList extends Wiget {
    constructor(parent) {
        super(parent)
        this.parent = parent
        this.id = 'tp-taskList'
        this.cacheServis = this.parent.cacheServis
        this.options = {innerText: 'На эту дату задач нет'}
        
        this.taskItemArray = this.initTaskItems()
    }

    initTaskItems() {
        let tasksToShow = this.taskArray
        if(tasksToShow){
            let itemsArray = []
            for (let task of tasksToShow) {
                let taskItem = new TaskItem(this, task)
                itemsArray.push(taskItem)
            }
            return itemsArray 
        }
    }

    build() {
        super.build()
        this.makeListObserver()
        this.buildTaskItems()

    }

    buildTaskItems() {
        if(this.taskItemArray){
            this.taskItemArray.forEach(taskitem => taskitem.build())
        }
    }

    makeListObserver() {
        // creates a MutationObserver object that keeps track of the number
        // of tasks items in the TaskList div. If it becomes 0, the message “all tasks
        // completed” will be displayed.
        const itemsObserver = new MutationObserver((mutationsList, observer) => {
            for (let mutation of mutationsList) { 
                if(!mutation.target.childElementCount) {
                    mutation.target.style.fontSize = '18px'
                } else {
                    mutation.target.style.fontSize = '0px'
                }
                return
            }
        })
        const observerConfig = {attributes: false, childList: true, subtree: false}
        itemsObserver.observe(this.element, observerConfig)
    }

    clear() {
        this.taskItemArray.forEach(taskitem => taskitem.remove())
    }

    update() {
        this.clear()
        this.taskItemArray = this.initTaskItems()
        this.buildTaskItems()
    }


    openTaskAdder() {
        let adder = new TaskAdder(this)
        this.taskItemArray.push(adder)
        adder.build()

    }

    get relatedDayButton() {
        return this.parent.relatedDayButton
    }

    get taskArray() {
        return this.parent.dailyTaskArray
    }

    get date() {
        return this.parent.relatedDayButton.date
    }

    get dateString() {
        return DateFormater.formatForBackend(this.date)
    }

}


class TaskItem extends Wiget {
    constructor(parent, taskObj) {
        super(parent)

        this.parent = parent
        this.cacheServis = this.parent.cacheServis
        this.taskObj = taskObj ? taskObj : this._empyTaskObj
        this.id = this.makeId('ti')
        this.element.className = 'tp-taskitem'

        // checkbox to mark the task as completed or vice versa
        this.checkDone = new Wiget(this, {
            className: 'tp-taskCheckout',
            type: 'checkbox',
            checked: this.taskObj.completion,
            onclick: this.checkUncheckCompletion.bind(this)
        }, 'input'),
        
        // container for a divs that displays the title and description of
        // the task or widgets for the user to edit the task
        this.Main = new Wiget(this, {
            className: 'tp-taskitemMain'
        })


        // divs that displays task's title and description
        this.defaultWigets = [
            this.Title = new Wiget(this.Main, {
                className: 'tp-taskitemTitle',
                innerText: this.taskObj.title
            }), 
            this.Description = new Wiget(this.Main, {
                className: 'tp-taskitemDescr',
                innerText: this.taskObj.description,
            }),
                
        ]

        // wigets for editing task fields (user input)
        this.editingWigets = [

            this.SaveCloseCont = new Wiget(this.Main, {
                className: 'tp-taskitemSaveClose',
            }),
                this.SaveButton = new iconButton24(this.SaveCloseCont, {
                    className: 'save_task',
                    onclick: this.saveInputValues.bind(this)
                }, iconSaveTask), 
                this.CloseEditorButton = new iconButton24(this.SaveCloseCont, {
                    className: 'closeEditor',
                    onclick: this.switchToDefaultMode.bind(this),
                }, iconCloseEditor),
        
            this.TaskTimeSettingsCont = new Wiget(this.Main, {
                className: 'tp-taskTimeSettings'
            }),           
                this.DateSetings = new TaskSettingsElement(this.TaskTimeSettingsCont,
                    'date', this.taskObj, 'Отложить:'),                    
                this.IntervalSettings = new TaskSettingsElement(this.TaskTimeSettingsCont,
                    'interval', this.taskObj, 'Повтор:'),                    
                this.AutoshiftSettings = new TaskSettingsElement(this.TaskTimeSettingsCont,
                    'autoshift', this.taskObj, 'Автоперенос:'),
        
            this.InputTitle = new TaskSettingsElement(this.Main, 'input', this.taskObj, 
                'Название задачи:'),
        
            this.InputDescription = new TaskSettingsElement(this.Main, 'textarea', this.taskObj,
                'Описание задачи:')
        ]
        
        // buttons 'edit task(switch to editor mode)' and 'delete task'
        // (located outside the task item's Main container)
        this.RightButtons = [
            this.RightButtonsCont = new Wiget(this, {
                className: 'tp-taskitemRightBtns'
            }),
                this.EditTaskButton = new iconButton24(this.RightButtonsCont, {
                    className: 'button-icon24',
                    onclick: this.switchToEditMode.bind(this)
                }, iconEditTask),
                this.DeleteTaskButton = new iconButton24(this.RightButtonsCont, {
                    className: 'button-icon24',
                    onclick: this.removeSelf.bind(this)
                }, iconDeleteTask)
        ]
    }

    build() {
        super.build()
        this.checkDone.build()
        this.Main.build()
        this.RightButtons.forEach(wg => wg.build())
        
        this.SaveButton.addCssClass('ti-SaveTaskBt')
        this.CloseEditorButton.addCssClass('ti-CloseEditorBt')
        this.DeleteTaskButton.addCssClass('tp-RightBtnsDelTask')
        this.EditTaskButton.addCssClass('tp-RightBtnsEditTask')
        
        this.defaultWigets.forEach(wg => wg.build())
    }

    switchToEditMode() {
        // hides a task's title and description divs and shows the widgets
        // for editing a task fields and options

        this.checkDone.hide()
        this.RightButtonsCont.hide()
        this.defaultWigets.forEach(wg => wg.hide())
        this.editingWigets.forEach(wg => {
            if(!wg.isBuilded()) {
                wg.build()
            } else {
                wg.show()
            }
        })
        this.makeConstraints()
    }

    switchToDefaultMode() {
        // hides a task's title and description divs and shows the widgets for
        // editing a task fields and options

        this.checkDone.show()
        this.defaultWigets.forEach(wg => wg.show())
        this.editingWigets.forEach(wg => wg.hide())
        this.RightButtonsCont.show()
    }

    removeSelf() {
        // remove the task-item wiget from task list wiget and deletes related enty
        // about the task in the database
        this.cacheServis.deleteTask(this.taskObj)
            .then(() => {
                this.remove()
                // if the task have interval repeat and we need to refresh
                // all of DayButtons on calendar wiget to deleted repeats 
                // that shouldn't exist anymore
                if(this.taskObj.interval) {
                    calendar.refreshMonth()
                } else {
                    this.relatedDayButton.updStatus()
                }
            })
            .catch(err => {
                throw err
            })
    }

    takeInputValues() {
        // returns the values of user input from a task editing widgets

        return {
            initdate: this.DateSetings.value + ' 00:00:00',
            date: this.DateSetings.value + ' 00:00:00',
            interval: this.IntervalSettings.value,
            autoshift: this.AutoshiftSettings.value,
            title: this.InputTitle.value,
            description: this.InputDescription.value
        }
    }

    updateFields(newTaskFields) {
        // Updates the text of the divs, that displaying a task's
        // title and description

        this.Title.element.innerText = newTaskFields.title
        this.Description.element.innerText = newTaskFields.description
    }

    makeConstraints() {
        // To avoid conflicting states, in a task editing mode:
        //     1) disables the wigets for date changing and "auto-postone untill
        // completion" when chosen one of a task's interval repeating options;
        //     2) disables the date changing and 'auto-postone untill completion' 
        // wigets when a task marked as completed in the task settings;
        //     3) disables the interval choosing wiget when 'postpone untill 
        // completion' option is active;  

        const dateInput = this.DateSetings.inputWiget
        const intervalInput = this.IntervalSettings.inputWiget
        const autoshiftInput = this.AutoshiftSettings.inputWiget
        const checkDone = this.checkDone.element

        if(intervalInput.value != 'no' || checkDone.checked) {
            dateInput.disable()
            autoshiftInput.disable()
        } else if(!checkDone.checked) {
            dateInput.enable()
            autoshiftInput.enable()
        }
        intervalInput.element.addEventListener('change', event => {
            if(event.target.value != 'no' && !checkDone.checked) {
                dateInput.disable()
                autoshiftInput.disable()
            } else if (!checkDone.checked) {
                dateInput.enable()
                autoshiftInput.enable()
            }
        })

        if(autoshiftInput.value != 'no') {
            intervalInput.disable()
        }
        autoshiftInput.element.addEventListener('change', event => {
            if(event.target.value != 'no') {
                intervalInput.disable()
            } else {
                intervalInput.enable()
            }
        })
    }

    saveInputValues() {
        // takes the user's input from the task editing widgets and push it
        // on the server via cacheService.edit Task() method. If server succeed,
        // updates appearance the application appropriately

        let newTaskFields = this.takeInputValues()
        newTaskFields.ID = this.taskObj.ID
                          
        this.cacheServis.editTask(newTaskFields)
            .then(() => {
                calendar.updDayButtonsStatus()
                taskPanel.TaskList.update()                    
            })
            .catch(err => {
                console.error(err)
            })
    }

    checkUncheckCompletion() {
        // sends user input from checkDone checkbox (which indicates whether
        // a task marked as completed or not) to the server. If server
        // responds with succeed, the appearance of the application will
        // appropriately updated

        let checkObject = {
                ID: this.taskObj.ID,
                date: this.taskObj.date,
        }

        if(this.checkDone.element.checked) {
            checkObject.completion = this.taskObj.date
        } else {
            checkObject.completion = false
        }
        this.cacheServis.checkUncheckTask(checkObject)
            .then(() => {
                this.relatedDayButton.updStatus()
            })
            //TODO: error catching

    }

    get relatedDayButton() {
        return this.parent.relatedDayButton
    }

    get _empyTaskObj() {
        return TaskObject.getEmpty({
            date: this.parent.dateString,
            initdate: this.parent.dateString,
        })
    }

}


class TaskAdder extends TaskItem {
    constructor(parent) {
        super(parent)
        this.id = this.makeId('ta')
    }

    build(){
        super.build()
        this.switchToEditMode()
        this.reBind()
        this.element.style.order = '-1'
    }

    reBind() {
        this.CloseEditorButton.element.onclick = this.remove.bind(this)
        this.SaveButton.element.onclick = this.createNewTask.bind(this)
    }

    createNewTask() {
        let newTask = this.takeInputValues()
        newTask.ID = this.taskObj.ID

        let thereIsInterval
        if(newTask.interval && newTask.interval != 'no'){
            thereIsInterval = true
        } else {
            thereIsInterval = false
        }
                          
        this.cacheServis.createTask(newTask)
            .then(() => {
                this.remove()
                calendar.updDayButtonsStatus()
                taskPanel.TaskList.update()
                if(thereIsInterval){
                    calendar.refreshMonth()
                }                  
            })
            .catch(err => {
                console.error(err)
            })
    }
}

class TaskSettingsElement extends Wiget {
    constructor(parent, inputType, taskObj, labelText) {
        super(parent)
        this.parent = parent
        this.element.className = 'tp-SettingsElement'
        this.taskObj = taskObj

        this.inputWiget = this.initInputWg(inputType)
        this.label = new Wiget(this, {innerText: labelText}, 'label')
    }

    build() {
        super.build()
        this.label.build()
        this.inputWiget.build()
    }

    get value() {
        return this.inputWiget.value
    }

    set value(defaultValue) {
        this.inputWiget.value = defaultValue
    }

    initInputWg(type) {
        if (type === 'date'){
            return new Wiget(this, {
                type: 'date',
                name: 'new_date',
                value: this.taskObj.initdate.slice(0,10),
            }, 'input')
        } else if (type === 'interval'){
            const inputWg = new Select(this, [
                ['no', 'нет'],
                ['every_day', 'ежедневно'],
                ['every_workday', 'по будням'],
                ['every_week', 'еженедельно'],
                ['every_month', 'ежемясячно'],
                ['every_year', 'ежегодно']
            ])
            inputWg.defaultValue = this.taskObj.interval
            return inputWg
        } else if (type === 'autoshift') {
            const inputWg = new Select(this, [
                ['no', 'нет'],
                ['yes', 'до выполнения']
            ])
            inputWg.defaultValue = this.taskObj.autoshift
            return inputWg
        } else if (type === 'input'){
            return new Wiget(this, {
                type: 'text', 
                name: 'new_title',
                maxlength: "80",
                minlength: "1",
                value: this.taskObj.title  
            }, 'input')
            return inputWg
        } else if (type === 'textarea') {
            return new Wiget(this, {
                name: 'newDescription',
                rows: '5',
                cols: '3',
                value: this.taskObj.description
            }, 'textarea')
        }
    }

    get value() {
        return this.inputWiget.element.value
    }

    set value(newValue) {
        this.inputWiget.element.value = newValue
    }

    get cacheServis() {
        return this.parent.cacheServis
    }

}


class Select extends Wiget {
    //  Constructor of the Wiget takes two args: parent Wiget and optionList.
    //  OptionsList arg should be represented as an array of arrays. 
    //  Each nested array must consists of two items: 
    //  1) value attr of html <option> element;
    //  2) inner text of <option>.
    constructor(parent, optionsList) {
        super(parent)
        this.tag = 'select'
        this.element = document.createElement(this.tag)
        this.optionsList = this.initOptions(optionsList)
        this.defaultValue
    }

    get value(){
        return this.element.value
    }

    set value(newValue){
        this.element.value = newValue
    }

    initOptions(optionsList) {
        let optionWigets = []
        optionsList.forEach(pair => {
            let value = pair[0]
            let text = pair[1]
            const optionWiget = new Wiget(this, {
                value: value,
                text: text
            }, 'option')
            optionWigets.push(optionWiget)
        })
        return optionWigets
    }

    build(){
        super.build()
        this.optionsList.forEach(opt => opt.build())
        
        if(this.defaultValue) {
            this.value = this.defaultValue
        }
    }
}


function copyObject(object) {
    let newCopy = {}
    Object.assign(newCopy, object)
    return newCopy
}


// Entire app launch initializations.
const mainContainer = document.getElementById('main-container')

const transportService = new TransportService()
const cacheServis = new CacheServis(transportService)
let calendar
let taskPanel
cacheServis.readyToRun
    .then( () => {
        calendar = new Calendar(mainContainer, cacheServis)
        calendar.build() 
        taskPanel = new TaskPanel(mainContainer, cacheServis)
        taskPanel.build()    
    })
    .catch(err => {
        console.error(err)
        alert(err.errorTraceback)
    })